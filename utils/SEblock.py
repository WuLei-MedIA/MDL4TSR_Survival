
import tensorflow as tf

def squeeze_excite_block(input, ratio=16):
    init = input #
    channel_axis = 1 if tf.keras.backend.image_data_format() == "channels_first" else -1
    filters = init.shape[channel_axis]
    se_shape = (1,1,filters)

    seb = tf.keras.layers.GlobalAveragePooling2D()(input)
    seb = tf.keras.layers.Reshape(se_shape)(seb)
    seb = tf.keras.layers.Dense(filters // ratio, activation="relu", kernel_initializer="he_normal", use_bias=False)(seb)
    seb = tf.keras.layers.Dense(filters, activation="sigmoid", kernel_initializer="he_normal", use_bias=False)(seb)

    if tf.keras.backend.image_data_format() == "channels_first":
        seb = tf.keras.layers.Permute((3,1,2))(seb)
    x = tf.keras.layers.multiply([init, seb])
    return x

def spatial_squeeze_excite_block(input):
    seb = tf.keras.layers.Conv2D(1, (1,1), activation="sigmoid", use_bias="False", kernel_initializer="he_normal")(input)
    x = tf.keras.layers.multiply([input, seb])
    return x

def channel_spatial_squeeze_excite(input, ratio=16):
    cse = squeeze_excite_block(input, ratio)
    sse = spatial_squeeze_excite_block(input)
    x = tf.keras.layers.add([cse, sse])
    return x



