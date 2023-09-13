

UnivariableCox_extract <- function(univ_models_list){
  lapply(univ_models_list,
         function(x){
           x <- summary(x)
           # print(x)
           # p.value<-signif(x$wald["pvalue"], digits=3)
           # wald.test<-signif(x$wald["test"], digits=3)
           p_value <- signif(x$coefficients[,"Pr(>|z|)"],4)
           beta<-signif(x$coef[,1], digits=4);#coeficient beta
           HR <-signif(x$coef[,2], digits=4);#exp(beta)
           HR.confint.lower <- signif(x$conf.int[,"lower .95"],4)
           HR.confint.upper <- signif(x$conf.int[,"upper .95"],4)
           HR <- paste0(HR, " (", 
                        HR.confint.lower, "-", HR.confint.upper, ")")
           #res<-c(beta, HR, p_value)
           res <- tibble(variablename=rownames(x$coefficients), beta=beta, HR=HR, pvalue=p_value) %>% 
             as.data.frame(.,row.names = F)
           #names(res)<-c("beta", "HR (95% CI for HR)", "wald.test", "p.value")
           return(res)
           #return(exp(cbind(coef(x),confint(x))))
         })
}