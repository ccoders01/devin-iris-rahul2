package com.mrm.modelregistry.repository;

import com.mrm.modelregistry.entity.RiskRatingEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface RiskRatingRepository extends JpaRepository<RiskRatingEntity, Long> {
    Optional<RiskRatingEntity> findByCode(String code);
}
