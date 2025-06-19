package com.mrm.modelregistry.repository;

import com.mrm.modelregistry.entity.Model;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
class ModelRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private ModelRepository modelRepository;

    @Test
    void save_ValidModel_ReturnsModelWithId() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Model savedModel = modelRepository.save(model);

        assertNotNull(savedModel);
        assertNotNull(savedModel.getId());
        assertEquals("Test Model", savedModel.getModelName());
        assertEquals("v1.0", savedModel.getModelVersion());
        assertEquals("Test Sponsor", savedModel.getModelSponsor());
        assertEquals(Model.BusinessLine.RETAIL_BANKING, savedModel.getBusinessLine());
        assertEquals(Model.ModelType.CREDIT_RISK, savedModel.getModelType());
        assertEquals(Model.RiskRating.MEDIUM, savedModel.getRiskRating());
        assertEquals(Model.Status.IN_DEVELOPMENT, savedModel.getStatus());
        assertNotNull(savedModel.getCreatedAt());
        assertNotNull(savedModel.getUpdatedAt());
    }

    @Test
    void findById_ExistingId_ReturnsModel() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.MEDIUM,
            Model.Status.IN_DEVELOPMENT
        );

        Model savedModel = entityManager.persistAndFlush(model);

        Optional<Model> foundModel = modelRepository.findById(savedModel.getId());

        assertTrue(foundModel.isPresent());
        assertEquals("Test Model", foundModel.get().getModelName());
        assertEquals(savedModel.getId(), foundModel.get().getId());
    }

    @Test
    void findById_NonExistingId_ReturnsEmpty() {
        Optional<Model> foundModel = modelRepository.findById(999L);

        assertFalse(foundModel.isPresent());
    }

    @Test
    void findAll_ReturnsAllModels() {
        Model model1 = new Model(
            "Model 1",
            "v1.0",
            "Sponsor 1",
            Model.BusinessLine.RETAIL_BANKING,
            Model.ModelType.CREDIT_RISK,
            Model.RiskRating.HIGH,
            Model.Status.PRODUCTION
        );

        Model model2 = new Model(
            "Model 2",
            "v2.0",
            "Sponsor 2",
            Model.BusinessLine.INVESTMENT_BANKING,
            Model.ModelType.MARKET_RISK,
            Model.RiskRating.LOW,
            Model.Status.VALIDATED
        );

        entityManager.persistAndFlush(model1);
        entityManager.persistAndFlush(model2);

        List<Model> models = modelRepository.findAll();

        assertEquals(2, models.size());
        assertTrue(models.stream().anyMatch(m -> "Model 1".equals(m.getModelName())));
        assertTrue(models.stream().anyMatch(m -> "Model 2".equals(m.getModelName())));
    }

    @Test
    void findAll_EmptyRepository_ReturnsEmptyList() {
        List<Model> models = modelRepository.findAll();

        assertTrue(models.isEmpty());
    }
}
