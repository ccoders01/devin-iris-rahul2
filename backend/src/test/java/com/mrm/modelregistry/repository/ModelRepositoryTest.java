package com.mrm.modelregistry.repository;

import com.mrm.modelregistry.entity.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

@DataJpaTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.ANY)
class ModelRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private ModelRepository modelRepository;

    private BusinessLineEntity businessLine;
    private ModelTypeEntity modelType;
    private RiskRatingEntity riskRating;
    private StatusEntity status;

    @BeforeEach
    void setUp() {
        businessLine = new BusinessLineEntity("RETAIL_BANKING", "Retail Banking");
        businessLine = entityManager.persistAndFlush(businessLine);
        
        modelType = new ModelTypeEntity("CREDIT_RISK", "Credit Risk");
        modelType = entityManager.persistAndFlush(modelType);
        
        riskRating = new RiskRatingEntity("MEDIUM", "Medium");
        riskRating = entityManager.persistAndFlush(riskRating);
        
        status = new StatusEntity("IN_DEVELOPMENT", "In Development");
        status = entityManager.persistAndFlush(status);
    }

    @Test
    void contextLoads() {
        assertNotNull(entityManager);
        assertNotNull(modelRepository);
    }

    @Test
    void save_ValidModel_ReturnsModelWithId() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            businessLine,
            modelType,
            riskRating,
            status
        );

        Model savedModel = modelRepository.save(model);

        assertNotNull(savedModel);
        assertNotNull(savedModel.getId());
        assertEquals("Test Model", savedModel.getModelName());
        assertEquals("v1.0", savedModel.getModelVersion());
        assertEquals("Test Sponsor", savedModel.getModelSponsor());
        assertEquals(businessLine, savedModel.getBusinessLine());
        assertEquals(modelType, savedModel.getModelType());
        assertEquals(riskRating, savedModel.getRiskRating());
        assertEquals(status, savedModel.getStatus());
        assertNotNull(savedModel.getCreatedAt());
        assertNotNull(savedModel.getUpdatedAt());
    }

    @Test
    void findById_ExistingId_ReturnsModel() {
        Model model = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            businessLine,
            modelType,
            riskRating,
            status
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
            businessLine,
            modelType,
            riskRating,
            status
        );

        Model model2 = new Model(
            "Model 2",
            "v2.0",
            "Sponsor 2",
            businessLine,
            modelType,
            riskRating,
            status
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
