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
        log.info("Searching models with term: {}", searchTerm);
        
        if (!StringUtils.hasText(searchTerm)) {
            log.info("No search term provided, returning all models");
            return getAllModels();
        }
        
        String sql = buildDynamicSearchQuery();
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
        log.info("Retrieving all models using JdbcTemplate");
        
        String sql = "SELECT m.id, m.model_name, m.model_version, m.model_sponsor, " +
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
                    "ORDER BY m.id";
        
        List<ModelResponse> results = jdbcTemplate.query(sql, new ModelRowMapper());
        log.info("Retrieved {} models using JdbcTemplate", results.size());
        
        return results;
    }
    
    private String buildDynamicSearchQuery() {
        return "SELECT m.id, m.model_name, m.model_version, m.model_sponsor, " +
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
               "OR CAST(m.id AS CHAR) LIKE ?) " +
               "ORDER BY m.id";
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
