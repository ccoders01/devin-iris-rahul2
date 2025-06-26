package com.mrm.modelregistry.service;

import com.mrm.modelregistry.dto.ModelResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
@Slf4j
public class ModelSearchService {
    
    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    public List<ModelResponse> searchModels(String searchTerm) {
        return searchModels(searchTerm, null, "asc");
    }
    
    public List<ModelResponse> searchModels(String searchTerm, String sortBy, String sortDirection) {
        log.info("Searching models with term: {}, sortBy: {}, sortDirection: {}", searchTerm, sortBy, sortDirection);
        
        if (!StringUtils.hasText(searchTerm)) {
            log.info("No search term provided, returning all models with sorting");
            return getAllModels(sortBy, sortDirection);
        }
        
        String sql = buildSearchQuery(sortBy, sortDirection);
        String searchPattern = "%" + searchTerm.toLowerCase() + "%";
        
        log.debug("Executing search query: {} with pattern: {}", sql, searchPattern);
        
        List<Object> parameters = new ArrayList<>();
        for (int i = 0; i < 8; i++) {
            parameters.add(searchPattern);
        }
        
        List<ModelResponse> results = jdbcTemplate.query(sql, parameters.toArray(), new ModelRowMapper());
        log.info("Search returned {} results for term: {}", results.size(), searchTerm);
        
        return results;
    }
    
    public List<ModelResponse> getAllModels() {
        return getAllModels(null, "asc");
    }
    
    public List<ModelResponse> getAllModels(String sortBy, String sortDirection) {
        log.info("Retrieving all models using JdbcTemplate with sorting - sortBy: {}, sortDirection: {}", sortBy, sortDirection);
        
        String sql = buildSortedQuery(sortBy, sortDirection);
        
        List<ModelResponse> results = jdbcTemplate.query(sql, new ModelRowMapper());
        log.info("Retrieved {} models using JdbcTemplate", results.size());
        
        return results;
    }
    
    private String buildSortedQuery(String sortBy, String sortDirection) {
        String baseQuery = "SELECT m.id, m.model_name, m.model_version, m.model_sponsor, " +
                          "m.created_at, m.updated_at, " +
                          "bl.code as business_line_code, bl.display_name as business_line_display, " +
                          "mt.code as model_type_code, mt.display_name as model_type_display, " +
                          "rr.code as risk_rating_code, rr.display_name as risk_rating_display, " +
                          "s.code as status_code, s.display_name as status_display " +
                          "FROM models m " +
                          "JOIN business_lines bl ON m.business_line_id = bl.id " +
                          "JOIN model_types mt ON m.model_type_id = mt.id " +
                          "JOIN risk_ratings rr ON m.risk_rating_id = rr.id " +
                          "JOIN statuses s ON m.status_id = s.id ";
        
        return baseQuery + buildOrderByClause(sortBy, sortDirection);
    }
    
    private String buildSearchQuery(String sortBy, String sortDirection) {
        String baseQuery = "SELECT m.id, m.model_name, m.model_version, m.model_sponsor, " +
                          "m.created_at, m.updated_at, " +
                          "bl.code as business_line_code, bl.display_name as business_line_display, " +
                          "mt.code as model_type_code, mt.display_name as model_type_display, " +
                          "rr.code as risk_rating_code, rr.display_name as risk_rating_display, " +
                          "s.code as status_code, s.display_name as status_display " +
                          "FROM models m " +
                          "JOIN business_lines bl ON m.business_line_id = bl.id " +
                          "JOIN model_types mt ON m.model_type_id = mt.id " +
                          "JOIN risk_ratings rr ON m.risk_rating_id = rr.id " +
                          "JOIN statuses s ON m.status_id = s.id " +
                          "WHERE (LOWER(m.model_name) LIKE ? " +
                          "OR LOWER(m.model_version) LIKE ? " +
                          "OR LOWER(m.model_sponsor) LIKE ? " +
                          "OR LOWER(bl.display_name) LIKE ? " +
                          "OR LOWER(mt.display_name) LIKE ? " +
                          "OR LOWER(rr.display_name) LIKE ? " +
                          "OR LOWER(s.display_name) LIKE ? " +
                          "OR CAST(m.id AS CHAR) LIKE ?) ";
        
        return baseQuery + buildOrderByClause(sortBy, sortDirection);
    }
    
    private String buildOrderByClause(String sortBy, String sortDirection) {
        if (!StringUtils.hasText(sortBy)) {
            return "ORDER BY m.id DESC";
        }
        
        String direction = "DESC".equalsIgnoreCase(sortDirection) ? "DESC" : "ASC";
        
        return switch (sortBy.toLowerCase()) {
            case "id" -> "ORDER BY m.id " + direction;
            case "modelname" -> "ORDER BY m.model_name " + direction;
            case "modelversion" -> "ORDER BY m.model_version " + direction;
            case "modelsponsor" -> "ORDER BY m.model_sponsor " + direction;
            case "businessline" -> "ORDER BY bl.display_name " + direction;
            case "modeltype" -> "ORDER BY mt.display_name " + direction;
            case "riskrating" -> "ORDER BY rr.display_name " + direction;
            case "status" -> "ORDER BY s.display_name " + direction;
            case "createdat" -> "ORDER BY m.created_at " + direction;
            default -> "ORDER BY m.id DESC";
        };
    }
    
    private String buildDynamicSearchQuery() {
        return buildSearchQuery(null, "asc");
    }
    
    private static class ModelRowMapper implements RowMapper<ModelResponse> {
        @Override
        public ModelResponse mapRow(ResultSet rs, int rowNum) throws SQLException {
            ModelResponse response = new ModelResponse();
            response.setId(rs.getLong("id"));
            response.setModelName(rs.getString("model_name"));
            response.setModelVersion(rs.getString("model_version"));
            response.setModelSponsor(rs.getString("model_sponsor"));
            response.setBusinessLine(rs.getString("business_line_code"));
            response.setBusinessLineDisplayName(rs.getString("business_line_display"));
            response.setModelType(rs.getString("model_type_code"));
            response.setModelTypeDisplayName(rs.getString("model_type_display"));
            response.setRiskRating(rs.getString("risk_rating_code"));
            response.setRiskRatingDisplayName(rs.getString("risk_rating_display"));
            response.setStatus(rs.getString("status_code"));
            response.setStatusDisplayName(rs.getString("status_display"));
            response.setCreatedAt(rs.getObject("created_at", LocalDateTime.class));
            response.setUpdatedAt(rs.getObject("updated_at", LocalDateTime.class));
            return response;
        }
    }
}
