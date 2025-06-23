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

  getAllModels(): Observable<ModelResponse[]> {
    return this.http.get<ModelResponse[]>(this.apiUrl);
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
