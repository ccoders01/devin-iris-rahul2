package com.mrm.modelregistry.dto;

import com.mrm.modelregistry.entity.Model;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.*;

class ModelResponseTest {

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
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
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
        assertEquals(Model.BusinessLine.RETAIL_BANKING, response.getBusinessLine());
        assertEquals(Model.ModelType.CREDIT_RISK, response.getModelType());
        assertEquals(Model.RiskRating.MEDIUM, response.getRiskRating());
        assertEquals(Model.Status.IN_DEVELOPMENT, response.getStatus());
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
        response.setBusinessLine(Model.BusinessLine.RETAIL_BANKING);
        response.setModelType(Model.ModelType.CREDIT_RISK);
        response.setRiskRating(Model.RiskRating.MEDIUM);
        response.setStatus(Model.Status.IN_DEVELOPMENT);

        LocalDateTime now = LocalDateTime.now();
        response.setCreatedAt(now);
        response.setUpdatedAt(now);

        assertEquals(1L, response.getId());
        assertEquals("Test Model", response.getModelName());
        assertEquals("v1.0", response.getModelVersion());
        assertEquals("Test Sponsor", response.getModelSponsor());
        assertEquals(Model.BusinessLine.RETAIL_BANKING, response.getBusinessLine());
        assertEquals(Model.ModelType.CREDIT_RISK, response.getModelType());
        assertEquals(Model.RiskRating.MEDIUM, response.getRiskRating());
        assertEquals(Model.Status.IN_DEVELOPMENT, response.getStatus());
        assertEquals(now, response.getCreatedAt());
        assertEquals(now, response.getUpdatedAt());
    }

    @Test
    void constructor_WithModelHavingAllEnumValues_WorksCorrectly() {
        Model.BusinessLine[] businessLines = Model.BusinessLine.values();
        Model.ModelType[] modelTypes = Model.ModelType.values();
        Model.RiskRating[] riskRatings = Model.RiskRating.values();
        Model.Status[] statuses = Model.Status.values();

        for (Model.BusinessLine bl : businessLines) {
            for (Model.ModelType mt : modelTypes) {
                for (Model.RiskRating rr : riskRatings) {
                    for (Model.Status s : statuses) {
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

                        assertEquals(bl, response.getBusinessLine());
                        assertEquals(mt, response.getModelType());
                        assertEquals(rr, response.getRiskRating());
                        assertEquals(s, response.getStatus());
                    }
                }
            }
        }
    }
}
