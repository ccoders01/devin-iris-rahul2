export interface ModelRequest {
  modelName: string;
  modelVersion: string;
  modelSponsor: string;
  businessLine: BusinessLine;
  modelType: ModelType;
  riskRating: RiskRating;
  status: Status;
}

export interface ModelResponse {
  id: number;
  modelName: string;
  modelVersion: string;
  modelSponsor: string;
  businessLine: BusinessLine;
  modelType: ModelType;
  riskRating: RiskRating;
  status: Status;
  createdAt: string;
  updatedAt: string;
}

export enum BusinessLine {
  RETAIL_BANKING = 'RETAIL_BANKING',
  WHOLESALE_LENDING = 'WHOLESALE_LENDING',
  INVESTMENT_BANKING = 'INVESTMENT_BANKING',
  RISK_MANAGEMENT = 'RISK_MANAGEMENT'
}

export enum ModelType {
  CREDIT_RISK = 'CREDIT_RISK',
  MARKET_RISK = 'MARKET_RISK',
  OPERATIONAL_RISK = 'OPERATIONAL_RISK',
  AML = 'AML',
  CAPITAL_CALCULATION = 'CAPITAL_CALCULATION',
  VALUATION = 'VALUATION'
}

export enum RiskRating {
  HIGH = 'HIGH',
  MEDIUM = 'MEDIUM',
  LOW = 'LOW'
}

export enum Status {
  IN_DEVELOPMENT = 'IN_DEVELOPMENT',
  VALIDATED = 'VALIDATED',
  PRODUCTION = 'PRODUCTION',
  RETIRED = 'RETIRED'
}

export interface EnumOption {
  value: string;
  displayName: string;
}

export interface EnumValues {
  businessLines: EnumOption[];
  modelTypes: EnumOption[];
  riskRatings: EnumOption[];
  statuses: EnumOption[];
}
