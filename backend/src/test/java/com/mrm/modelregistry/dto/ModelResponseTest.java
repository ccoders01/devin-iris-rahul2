package com.mrm.modelregistry.dto;

import com.mrm.modelregistry.entity.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class ModelResponseTest {

    private BusinessLineEntity businessLine;
    private ModelTypeEntity modelType;
    private RiskRatingEntity riskRating;
    private StatusEntity status;

    @BeforeEach
    void setUp() {
        businessLine = new BusinessLineEntity("RETAIL_BANKING", "Retail Banking");
        modelType = new ModelTypeEntity("CREDIT_RISK", "Credit Risk");
        riskRating = new RiskRatingEntity("MEDIUM", "Medium");
        status = new StatusEntity("IN_DEVELOPMENT", "In Development");
    }

    @Test
    void defaultConstructor_CreatesEmptyModelResponse() {
        ModelResponse response = new ModelResponse();

        assertNull(response.getId());
        assertNull(response.getModelName());
        assertNull(response.getModelVersion());
        assertNull(response.getModelSponsor());
        assertNull(response.getBusinessLine());
        assertNull(response.getModelType());
        assertNull(response.getRiskRating());
        assertNull(response.getStatus());
        assertNull(response.getCreatedAt());
        assertNull(response.getUpdatedAt());
    }

    @Test
    void constructor_WithModel_CopiesAllFields() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            businessLine,
            modelType,
            riskRating,
            status
        );
        model.setId(1L);

        LocalDateTime now = LocalDateTime.now();
        model.setCreatedAt(now);
        model.setUpdatedAt(now);

        ModelResponse response = new ModelResponse(model);

        assertEquals(1L, response.getId());
        assertEquals("Test Model", response.getModelName());
        assertEquals("v1.0", response.getModelVersion());
        assertEquals("Test Sponsor", response.getModelSponsor());
        assertEquals("RETAIL_BANKING", response.getBusinessLine());
        assertEquals("CREDIT_RISK", response.getModelType());
        assertEquals("MEDIUM", response.getRiskRating());
        assertEquals("IN_DEVELOPMENT", response.getStatus());
        assertEquals(now, response.getCreatedAt());
        assertEquals(now, response.getUpdatedAt());
    }

    @Test
    void constructor_WithNullModel_HandlesGracefully() {
        assertThrows(NullPointerException.class, () -> {
            new ModelResponse(null);
        });
    }

    @Test
    void gettersAndSetters_WorkCorrectly() {
        ModelResponse response = new ModelResponse();

        response.setId(1L);
        response.setModelName("Test Model");
        response.setModelVersion("v1.0");
        response.setModelSponsor("Test Sponsor");
        response.setBusinessLine("RETAIL_BANKING");
        response.setModelType("CREDIT_RISK");
        response.setRiskRating("MEDIUM");
        response.setStatus("IN_DEVELOPMENT");

        LocalDateTime now = LocalDateTime.now();
        response.setCreatedAt(now);
        response.setUpdatedAt(now);

        assertEquals(1L, response.getId());
        assertEquals("Test Model", response.getModelName());
        assertEquals("v1.0", response.getModelVersion());
        assertEquals("Test Sponsor", response.getModelSponsor());
        assertEquals("RETAIL_BANKING", response.getBusinessLine());
        assertEquals("CREDIT_RISK", response.getModelType());
        assertEquals("MEDIUM", response.getRiskRating());
        assertEquals("IN_DEVELOPMENT", response.getStatus());
        assertEquals(now, response.getCreatedAt());
        assertEquals(now, response.getUpdatedAt());
    }

    @Test
    void constructor_WithModelHavingDifferentEntityValues_WorksCorrectly() {
        BusinessLineEntity[] businessLines = {
            new BusinessLineEntity("RETAIL_BANKING", "Retail Banking"),
            new BusinessLineEntity("INVESTMENT_BANKING", "Investment Banking")
        };
        ModelTypeEntity[] modelTypes = {
            new ModelTypeEntity("CREDIT_RISK", "Credit Risk"),
            new ModelTypeEntity("MARKET_RISK", "Market Risk")
        };
        RiskRatingEntity[] riskRatings = {
            new RiskRatingEntity("HIGH", "High"),
            new RiskRatingEntity("MEDIUM", "Medium")
        };
        StatusEntity[] statuses = {
            new StatusEntity("IN_DEVELOPMENT", "In Development"),
            new StatusEntity("PRODUCTION", "Production")
        };

        for (BusinessLineEntity bl : businessLines) {
            for (ModelTypeEntity mt : modelTypes) {
                for (RiskRatingEntity rr : riskRatings) {
                    for (StatusEntity s : statuses) {
                        Model model = new Model(
                            "Test Model",
                            "v1.0",
                            "Test Sponsor",
                            bl,
                            mt,
                            rr,
                            s
                        );
                        model.setId(1L);

                        ModelResponse response = new ModelResponse(model);

                        assertEquals(bl.getCode(), response.getBusinessLine());
                        assertEquals(mt.getCode(), response.getModelType());
                        assertEquals(rr.getCode(), response.getRiskRating());
                        assertEquals(s.getCode(), response.getStatus());
                    }
                }
            }
        }
    }
}
