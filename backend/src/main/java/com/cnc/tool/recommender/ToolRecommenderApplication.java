package com.cnc.tool.recommender;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
@ConfigurationPropertiesScan
public class ToolRecommenderApplication {

    public static void main(String[] args) {
        SpringApplication.run(ToolRecommenderApplication.class, args);
    }
} 