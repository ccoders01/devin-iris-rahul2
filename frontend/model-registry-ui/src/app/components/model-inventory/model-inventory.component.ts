import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ModelService } from '../../services/model.service';
import { ModelResponse, ModelRequest, EnumValues } from '../../models/model.interface';

@Component({
  selector: 'app-model-inventory',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './model-inventory.component.html',
  styleUrls: ['./model-inventory.component.css']
})
export class ModelInventoryComponent implements OnInit {
  models: ModelResponse[] = [];
  filteredModels: ModelResponse[] = [];
  searchTerm: string = '';
  sortBy: string = '';
  sortDirection: string = 'asc';
  totalCount: number = 0;
  isLoading = true;
  errorMessage = '';
  editingModelId: number | null = null;
  editForm: FormGroup | null = null;
  enumValues: EnumValues | null = null;

  constructor(
    private modelService: ModelService,
    private router: Router,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.loadModels();
    this.loadEnumValues();
  }

  loadModels(): void {
    this.isLoading = true;
    this.errorMessage = '';
    
    this.modelService.getAllModels(this.searchTerm || undefined, this.sortBy || undefined, this.sortDirection).subscribe({
      next: (response) => {
        if (Array.isArray(response)) {
          this.models = response;
          this.filteredModels = [...response];
          this.totalCount = response.length;
        } else {
          this.models = response.models || [];
          this.filteredModels = [...(response.models || [])];
          this.totalCount = response.totalCount || 0;
        }
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading models:', error);
        this.errorMessage = 'Failed to load models. Please try again.';
        this.isLoading = false;
      }
    });
  }

  loadEnumValues(): void {
    this.modelService.getEnumValues().subscribe({
      next: (data) => {
        this.enumValues = data;
      },
      error: (error) => {
        console.error('Error loading enum values:', error);
      }
    });
  }

  onSearchChange(searchTerm: string): void {
    this.searchTerm = searchTerm;
    this.isLoading = true;
    
    this.modelService.getAllModels(searchTerm.trim() || undefined, this.sortBy || undefined, this.sortDirection).subscribe({
      next: (response) => {
        if (Array.isArray(response)) {
          this.models = response;
          this.filteredModels = [...response];
          this.totalCount = response.length;
        } else {
          this.models = response.models || [];
          this.filteredModels = [...(response.models || [])];
          this.totalCount = response.totalCount || 0;
        }
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error searching models:', error);
        this.errorMessage = 'Failed to search models. Please try again.';
        this.isLoading = false;
      }
    });
  }

  private filterModels(): void {
    this.filteredModels = [...this.models];
  }

  startEdit(model: ModelResponse): void {
    this.editingModelId = model.id;
    this.editForm = this.fb.group({
      modelName: [model.modelName, [Validators.required]],
      modelVersion: [model.modelVersion, [Validators.required]],
      modelSponsor: [model.modelSponsor, [Validators.required]],
      businessLine: [model.businessLine, [Validators.required]],
      modelType: [model.modelType, [Validators.required]],
      riskRating: [model.riskRating, [Validators.required]],
      status: [model.status, [Validators.required]]
    });
  }

  saveEdit(): void {
    if (this.editForm?.valid && this.editingModelId) {
      const modelRequest: ModelRequest = this.editForm.value;
      this.modelService.updateModel(this.editingModelId, modelRequest).subscribe({
        next: (response) => {
          this.loadModels();
          this.cancelEdit();
        },
        error: (error) => {
          console.error('Error updating model:', error);
          this.errorMessage = 'Failed to update model. Please try again.';
        }
      });
    }
  }

  cancelEdit(): void {
    this.editingModelId = null;
    this.editForm = null;
  }

  refreshModels(): void {
    this.loadModels();
  }
  
  onSort(column: string): void {
    if (this.sortBy === column) {
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortBy = column;
      this.sortDirection = 'asc';
    }
    this.loadModels();
  }



  getSortIcon(column: string): string {
    if (this.sortBy !== column) return '↕️';
    return this.sortDirection === 'asc' ? '↑' : '↓';
  }
  
  get Math() {
    return Math;
  }

  navigateToRegistration(): void {
    this.router.navigate(['/register']);
  }

  getDisplayValue(enumValue: string): string {
    return enumValue.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase());
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  }
}
