

import tensorflow as tf
from tensorflow.keras import regularizers
from utils.SEblock import channel_spatial_squeeze_excite

reg_weight = 0.02
def conv_block(input, filters, name_prefix):
    """
    :param input: 
    :param filters: 
    :param name_prefix:
    :return:
    """
    layer = tf.keras.layers.Conv2D(filters, kernel_size=1, strides=1,padding='same', kernel_initializer='he_normal',
                                   name=name_prefix+"Conv1", use_bias=False)(input)
    layer = tf.keras.layers.BatchNormalization()(layer)
    layer = tf.keras.layers.ReLU()(layer)

    layer = tf.keras.layers.Conv2D(filters, kernel_size=3, strides=1,padding='same', kernel_initializer='he_normal',
                                   name=name_prefix+"Conv2", use_bias=False)(layer)
    layer = tf.keras.layers.BatchNormalization()(layer)
    layer = tf.keras.layers.ReLU()(layer)

    layer = tf.keras.layers.Conv2D(filters * 4, kernel_size=1, strides=1,padding='same', kernel_initializer='he_normal',
                                   name=name_prefix+"Conv3", use_bias=False)(layer)
    layer = tf.keras.layers.BatchNormalization()(layer)
    layer = tf.keras.layers.ReLU()(layer)
    return layer



def SE_ResNet50_Autoencoder( input_h,input_w,input_c, autolayers):
    model_input = tf.keras.layers.Input(shape=(input_h,input_w,input_c),name='images')
    identity_blocks = [3, 4, 6, 3]
    
    # Block 1
    layer = tf.keras.layers.Conv2D(filters=64, kernel_size=(7,7), strides=2, padding="same", kernel_initializer='he_normal',
                                   use_bias=False, name='block1_conv1')(model_input) 
    layer = tf.keras.layers.BatchNormalization()(layer)
    layer = tf.keras.layers.ReLU()(layer)
    block_1 = tf.keras.layers.MaxPooling2D(3, strides=2, padding="same", name='Block1_pool1')(layer) 
    

    # Block 2
    block_2 = conv_block(block_1, 64, "block2_0") 
    block_2 = channel_spatial_squeeze_excite(block_2, ratio=32.0)
    for i in range(1,identity_blocks[0]):
        block_2 = conv_block(block_2, 64, "block2_"+str(i)+"_")
        block_2 = channel_spatial_squeeze_excite(block_2, ratio=32.0) 
    

    # Block 3
    block_3 = tf.keras.layers.Conv2D(256, kernel_size=1, strides=2,kernel_initializer='he_normal',
                                     use_bias=False, name='block_3_conv0')(block_2) 
    block_3 = conv_block(block_3, 128, "block3_0")
    block_3 = channel_spatial_squeeze_excite(block_3, ratio=32.0)
    for i in range(1, identity_blocks[1]):
        block_3 = conv_block(block_3, 128, "block3_"+str(i)+"_")
        block_3 = channel_spatial_squeeze_excite(block_3, ratio=32.0) 
    

    # Block 4
    block_4 = tf.keras.layers.Conv2D(512, kernel_size=1, strides=2, kernel_initializer='he_normal',
                                     use_bias=False, name='block_4_conv0')(block_3) 
    block_4 = conv_block(block_4, 256, "block4_0") 
    block_4 = channel_spatial_squeeze_excite(block_4, ratio=32.0)
    for i in range(1, identity_blocks[2]):
        block_4 = conv_block(block_4, 256, "block4_"+str(i)+"_")
        block_4 = channel_spatial_squeeze_excite(block_4, ratio=32.0) 
    

    # Block 5
    block_5 = tf.keras.layers.Conv2D(1024, kernel_size=1, strides=2, kernel_initializer='he_normal',
                                     use_bias=False, name='block_5_conv0')(block_4)  
    block_5 = conv_block(block_5, 512, "block5_0") 
    block_5 = channel_spatial_squeeze_excite(block_5, ratio=32.0)
    for i in range(1, identity_blocks[2]):
        block_5 = conv_block(block_5, 512, "block5_"+str(i)+"_")
        block_5 = channel_spatial_squeeze_excite(block_5, ratio=32.0)
    # print("SE_ResNet50 block_5 shape: ", block_5.shape)

    va_block_2 = VAblock(block_2, 256, 1)  
    va_block_3 = VAblock(block_3, 512, 2)   
    va_block_4 = VAblock(block_4, 1024, 3) 
    va_block_5 = VAblock(block_5, 2048, 4)  

    feature_block1 = tf.keras.layers.GlobalAveragePooling2D()(va_block_2)
    feature_block2 = tf.keras.layers.GlobalAveragePooling2D()(va_block_3)
    feature_block3 = tf.keras.layers.GlobalAveragePooling2D()(va_block_4)
    feature_block4 = tf.keras.layers.GlobalAveragePooling2D()(va_block_5)
    x_concat = tf.keras.layers.concatenate([feature_block1,feature_block2,feature_block3,feature_block4], axis=-1)
    features = tf.keras.layers.Flatten()(x_concat)

    # Autoencoder
    encoder = tf.keras.layers.Dense(autolayers[0])(features)
    encoder = tf.keras.layers.BatchNormalization()(encoder)
    encoder = tf.keras.layers.LeakyReLU()(encoder)

    encoder = tf.keras.layers.Dense(autolayers[1])(encoder)
    encoder = tf.keras.layers.BatchNormalization()(encoder)
    encoder = tf.keras.layers.LeakyReLU()(encoder)

    bottleneck = tf.keras.layers.Dense(autolayers[2], name="Bottleneck")(encoder)

    decoder = tf.keras.layers.Dense(autolayers[1])(bottleneck)
    decoder = tf.keras.layers.BatchNormalization()(decoder)
    decoder = tf.keras.layers.LeakyReLU()(decoder)

    decoder = tf.keras.layers.Dense(autolayers[0])(decoder)
    decoder = tf.keras.layers.BatchNormalization()(decoder)
    decoder = tf.keras.layers.LeakyReLU()(decoder)

    decoder = tf.keras.layers.Dense(features.shape[-1])(decoder)

    x_dense1 = tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(reg_weight), name="Dense1")(bottleneck)
    x_batchNorm6 = tf.keras.layers.BatchNormalization(name="BatchNorm6")(x_dense1)
    x_dense2 = tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(reg_weight),name="Dense2")(x_batchNorm6)
    pred = tf.keras.layers.LeakyReLU()(x_dense2)
    pred = tf.keras.layers.Dropout(rate=0.2)(pred)
    pred_score = tf.keras.layers.Dense(1, activation=None, kernel_regularizer=regularizers.l2(reg_weight), name="pred_score")(pred)
    prediction = tf.keras.layers.Activation("sigmoid", name='class_prediction')(pred_score)
    x_dense3 = tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(reg_weight),name="Dense3")(x_batchNorm6)
    hazard_ratio1 = tf.keras.layers.Dense(1, activation=None, kernel_regularizer=regularizers.l2(reg_weight),name="Dense4")(x_dense3)
    hazard_ratio = tf.keras.layers.LeakyReLU(alpha=-1, name="hazard_ratio")(hazard_ratio1)
    model = tf.keras.Model(inputs=model_input, outputs=[features, decoder, hazard_ratio, prediction])
    return model






