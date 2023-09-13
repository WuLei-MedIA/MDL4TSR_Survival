


plot_KMCurves <- function(dframe, surv_time, surv_status, surv_var, legend_prefix, y_axis_prefix){
  # surv_time: string
  # surv_status: string
  # surv_var: string
  # legend_prefix: string
  
  library(survcomp)
  library(survminer)
  set.seed(seed)
  fit_cutoff_dframe <- survminer::surv_cutpoint(dframe, time = surv_time, event = surv_status, variables = surv_var)
  fit_cat_dframe <- survminer::surv_categorize(fit_cutoff_dframe)
  model_fit_dframe <- survminer::surv_fit(as.formula(paste( "Surv(", surv_time, "," , surv_status, ") ~", surv_var )), data = fit_cat_dframe)
  
  coxmodel_dframe <-  survival::coxph(as.formula(paste( "Surv(", surv_time, "," , surv_status, ") ~", surv_var )), data = dframe)
  surv_diff_dframe <- survminer::surv_pvalue(model_fit_dframe, method = "log-rank") 
  cox_HR_dframe <- tableone::ShowRegTable(coxmodel_dframe, digits = 3, printToggle=F)
  pvalue_dframe <- cox_HR_dframe[1] %>% str_replace(.,"\\[","\\(") %>% str_replace(.,"\\]","\\)") %>% str_replace(.,"\\, ","-")
  surv_text <- glue::glue("{surv_diff_dframe$pval.txt}
                        HR: {pvalue_dframe}")
  ggsurv_dframe <- survminer::ggsurvplot(model_fit_dframe, data = fit_cat_dframe, size=1.5,
                                         risk.table = "absolute",
                                         legend.title = " ",
                                         legend=c(0.1,0.50),
                                         legend.labs = c("Chemotherapy", "No Chemotherapy"),
                                         ylab= paste(y_axis_prefix,"survival",sep=" "),
                                         xlab= "Time (years)",
                                         break.time.by= 2,
                                         conf.int = T,
                                         censor.shape = "|",
                                         censor.size = 3,
                                         palette = c("#E71A11", "#1A94BE"),
                                         risk.table.title = "Number at risk:",
                                         risk.table.col = "strata",
                                         risk.table.y.text = T,
                                         risk.table.y.text.col = T,
                                         risk.table.fontsize = 7,
                                         risk.table.height = .25, 
                                         risk.table.pos='out',
                                         tables.theme = theme_cleantable(),
                                         )
  
  ggsurv_dframe$plot <- ggsurv_dframe$plot + 
    theme(panel.grid.major = element_blank(),panel.grid.minor = element_blank(), 
          panel.background = element_blank(),
          text=element_text(family="Arial", size=20),
          axis.line.x=element_line(linetype=1,color="black",size=1),
          axis.ticks.x=element_line(color="black",size=1,lineend = 1),
          axis.text.x=element_text(size=20,colour="black", family = "Arial", margin=unit(c(0.1,0.1,0.1,0.1), "cm")),
          axis.title.x = element_text(size=20,colour="black",margin=unit(c(0.1,0.1,0.2,0.1), "cm")),
          axis.line.y=element_line(linetype=1,color="black",size=1),
          axis.ticks.y=element_line(color="black",size=1,lineend = 1),
          axis.ticks.length = unit(0.4,"cm"),
          axis.text.y = element_text(size=20,colour="black", family = "Arial", margin=unit(c(0.1,0.1,0.1,0.1), "cm")),
          axis.title.y = element_text(size=20,colour="black",margin=unit(c(0.1,0.1,0.1,0.2), "cm")),
          legend.position = c(0.39,0.4), 
          legend.box = "vertical",
          legend.key.height = unit(1.5,"line"),
          legend.key.size = unit(2,"lines"),
          legend.key = element_rect(colour = NA, fill = NA),
          legend.text = element_text(size = 20,family = "Arial"),
          legend.title = element_blank())+
    annotate("text",  x = 0, y = 0.1, label = surv_text, size = 7, hjust = 0, family = "Arial")
  
  ggsurv_dframe$table <- ggsurv_dframe$table + 
    theme(
      axis.text.y = element_blank(),
      axis.ticks.y = element_blank(),
      # axis.line.x=element_line(linetype=1,color="black",size=1),
      # axis.ticks.x=element_line(color="black",size=1,lineend = 1),
      # axis.text.x=element_text(size=20,colour="black", family = "Arial", margin=unit(c(0.1,0.1,0.1,0.1), "cm")),
      # axis.title.x = element_text(size=20,colour="black",margin=unit(c(0.1,0.1,0.2,0.1), "cm")),
      # axis.line.y=element_line(linetype=1,color="black",size=1),
      # axis.ticks.y=element_line(color="black",size=1,lineend = 1),
      # axis.text.y = element_text(size=20,colour="black", family = "Arial"),
      # axis.title.y = element_text(size=20,colour="black",margin=unit(c(0.1,0.1,0.1,0.2), "cm")),
      
      plot.title = element_text(family = "Arial", size = 20, hjust = -0.19)
    )
  return(ggsurv_dframe)
}


