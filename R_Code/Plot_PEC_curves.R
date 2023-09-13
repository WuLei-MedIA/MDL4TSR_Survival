

plt_pec_curve <- function(PredError){
  library(tidyr)
  library(dplyr)
  df <- do.call(cbind, PredError[["AppErr"]]) 
  df <- cbind(PredError[["time"]], df) 
  colnames(df)[1] <- "time"             
  df <- as.data.frame(df) %>% tidyr::pivot_longer(cols = 2:last_col(), names_to = "models", values_to = "values") 
  df <- df %>% mutate(Amodel=ifelse(models=="Reference","A", ifelse(models=="Clinical Model","B", ifelse(models=="DL Model","C","D"))))
  df$Amodel <- factor(df$Amodel, levels = c("A","B", "C", "D"),
                      labels = c("Reference","Clinical Model", "DL Model", "Clinical+DL") )
  
  ggplot(data = df, aes(x = time, y = values, group=Amodel, color=Amodel)) + 
    geom_line(size=2) + 
    xlab("Time") + ylab("Prediction error") +
    theme(legend.key = element_blank())+theme(legend.background = element_blank())+
    scale_colour_manual(name = "", 
                        values=c("#999999", "#F29727", "#1A94BE","#E71A11"),) +
    theme(panel.grid.major = element_blank(),panel.grid.minor = element_blank(), 
          panel.background = element_blank(),
          text=element_text(family="Arial", size=20),
          axis.line.x=element_line(linetype=1.5,color="black",size=1),
          axis.ticks.x=element_line(color="black",size=1,lineend = 1),
          axis.text.x=element_text(size=20,colour="black", family = "Arial", margin=unit(c(0.1,0.1,0.1,0.1), "cm")),
          axis.title.x = element_text(size=20,colour="black",margin=unit(c(0.1,0.1,0.2,0.1), "cm")),
          axis.line.y=element_line(linetype=1,color="black",size=1),
          axis.ticks.y=element_line(color="black",size=1,lineend = 1),
          axis.ticks.length = unit(0.4,"cm"),
          axis.text.y = element_text(size=20,colour="black", family = "Arial", margin=unit(c(0.1,0.1,0.1,0.1), "cm")),
          axis.title.y = element_text(size=20,colour="black",margin=unit(c(0.1,0.1,0.1,0.2), "cm")),
          legend.position = c(0.2, 0.9),
          legend.box = "vertical",
          legend.key.height = unit(2,"line"),
          legend.key.size = unit(3,"lines"),
          legend.key = element_rect(colour = NA, fill = NA),
          legend.text = element_text(size = 20,family = "Arial"),
          legend.title = element_text(colour="black",size=20,family = "Arial"))
}


