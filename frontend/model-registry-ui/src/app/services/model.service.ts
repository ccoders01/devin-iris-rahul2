import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ModelRequest, ModelResponse, EnumValues } from '../models/model.interface';

@Injectable({
  providedIn: 'root'
})
export class ModelService {
  private apiUrl = 'http://localhost:8080/api/models';

  constructor(private http: HttpClient) { }

  registerModel(model: ModelRequest): Observable<ModelResponse> {
    return this.http.post<ModelResponse>(this.apiUrl, model);
  }

  getAllModels(searchTerm?: string, sortBy?: string, sortDirection?: string, page?: number, size?: number): Observable<any> {
    let params: any = {};
    if (searchTerm) params.search = searchTerm;
    if (sortBy) params.sortBy = sortBy;
    if (sortDirection) params.sortDirection = sortDirection;
    if (page !== undefined) params.page = page;
    if (size !== undefined) params.size = size;
    return this.http.get<any>(this.apiUrl, { params });
  }

  getModelById(id: number): Observable<ModelResponse> {
    return this.http.get<ModelResponse>(`${this.apiUrl}/${id}`);
  }

  getEnumValues(): Observable<EnumValues> {
    return this.http.get<EnumValues>(`${this.apiUrl}/enums`);
  }

  updateModel(id: number, model: ModelRequest): Observable<ModelResponse> {
    return this.http.put<ModelResponse>(`${this.apiUrl}/${id}`, model);
  }
}
