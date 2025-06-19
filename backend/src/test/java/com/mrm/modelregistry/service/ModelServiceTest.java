package com.mrm.modelregistry.service;

import com.mrm.modelregistry.dto.ModelRequest;
import com.mrm.modelregistry.dto.ModelResponse;
import com.mrm.modelregistry.entity.*;
import com.mrm.modelregistry.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class ModelServiceTest {

    @Mock
    private ModelRepository modelRepository;

    @Mock
    private BusinessLineRepository businessLineRepository;

    @Mock
    private ModelTypeRepository modelTypeRepository;

    @Mock
    private RiskRatingRepository riskRatingRepository;

    @Mock
    private StatusRepository statusRepository;

    @InjectMocks
    private ModelService modelService;

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
    void registerModel_ValidRequest_ReturnsModelResponse() {
        ModelRequest request = new ModelRequest(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            "RETAIL_BANKING",
            "CREDIT_RISK",
            "MEDIUM",
            "IN_DEVELOPMENT"
        );

        Model savedModel = new Model(
            "Test Model",
            "v1.0",
            "Test Sponsor",
            businessLine,
            modelType,
            riskRating,
            status
        );
        savedModel.setId(1L);
        savedModel.setCreatedAt(LocalDateTime.now());
        savedModel.setUpdatedAt(LocalDateTime.now());

        when(businessLineRepository.findByCode("RETAIL_BANKING")).thenReturn(Optional.of(businessLine));
        when(modelTypeRepository.findByCode("CREDIT_RISK")).thenReturn(Optional.of(modelType));
        when(riskRatingRepository.findByCode("MEDIUM")).thenReturn(Optional.of(riskRating));
        when(statusRepository.findByCode("IN_DEVELOPMENT")).thenReturn(Optional.of(status));
        when(modelRepository.save(any(Model.class))).thenReturn(savedModel);

        ModelResponse response = modelService.registerModel(request);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("Test Model", response.getModelName());
        assertEquals("v1.0", response.getModelVersion());
        assertEquals("Test Sponsor", response.getModelSponsor());
        assertEquals("RETAIL_BANKING", response.getBusinessLine());
        assertEquals("CREDIT_RISK", response.getModelType());
        assertEquals("MEDIUM", response.getRiskRating());
        assertEquals("IN_DEVELOPMENT", response.getStatus());

        verify(modelRepository, times(1)).save(any(Model.class));
        verify(businessLineRepository, times(1)).findByCode("RETAIL_BANKING");
        verify(modelTypeRepository, times(1)).findByCode("CREDIT_RISK");
        verify(riskRatingRepository, times(1)).findByCode("MEDIUM");
        verify(statusRepository, times(1)).findByCode("IN_DEVELOPMENT");
    }

    @Test
    void getAllModels_ReturnsModelResponseList() {
        Model model1 = new Model(
            "Model 1",
            "v1.0",
            "Sponsor 1",
            businessLine,
            modelType,
            new RiskRatingEntity("HIGH", "High"),
            new StatusEntity("PRODUCTION", "Production")
        );
        model1.setId(1L);

        Model model2 = new Model(
            "Model 2",
            "v2.0",
            "Sponsor 2",
            new BusinessLineEntity("INVESTMENT_BANKING", "Investment Banking"),
            new ModelTypeEntity("MARKET_RISK", "Market Risk"),
            new RiskRatingEntity("LOW", "Low"),
            new StatusEntity("VALIDATED", "Validated")
        );
        model2.setId(2L);

        List<Model> models = Arrays.asList(model1, model2);

        when(modelRepository.findAll()).thenReturn(models);

        List<ModelResponse> responses = modelService.getAllModels();

        assertNotNull(responses);
        assertEquals(2, responses.size());
        assertEquals("Model 1", responses.get(0).getModelName());
        assertEquals("Model 2", responses.get(1).getModelName());

        verify(modelRepository, times(1)).findAll();
    }

    @Test
    void getModelById_ExistingId_ReturnsModelResponse() {
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

        when(modelRepository.findById(1L)).thenReturn(Optional.of(model));

        ModelResponse response = modelService.getModelById(1L);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("Test Model", response.getModelName());

        verify(modelRepository, times(1)).findById(1L);
    }

    @Test
    void getModelById_NonExistingId_ThrowsException() {
        when(modelRepository.findById(999L)).thenReturn(Optional.empty());

        RuntimeException exception = assertThrows(RuntimeException.class, () -> {
            modelService.getModelById(999L);
        });

        assertEquals("Model not found with id: 999", exception.getMessage());
        verify(modelRepository, times(1)).findById(999L);
    }
}
