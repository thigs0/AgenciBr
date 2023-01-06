
            library(climatol)

            #------------------------------------------------------
            setwd("/home/thiagosilva/Downloads/teste")
            
            dat <- as.matrix(read.table("pr_2003-2021.dat"))
            write(dat, "Ttest_2003-2021.dat")
            
            homogen('pr', 2003, 2021, expl = TRUE)

            