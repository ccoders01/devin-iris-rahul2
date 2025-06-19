import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ModelService } from '../../services/model.service';
import { ModelResponse } from '../../models/model.interface';

@Component({
  selector: 'app-model-inventory',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './model-inventory.component.html',
  styleUrls: ['./model-inventory.component.css']
})
export class ModelInventoryComponent implements OnInit {
  models: ModelResponse[] = [];
  isLoading = true;
  errorMessage = '';

  constructor(
    private modelService: ModelService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadModels();
  }

  loadModels(): void {
    this.isLoading = true;
    this.errorMessage = '';
    
    this.modelService.getAllModels().subscribe({
      next: (data) => {
        this.models = data;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading models:', error);
        this.errorMessage = 'Failed to load models. Please try again.';
        this.isLoading = false;
      }
    });
  }

  refreshModels(): void {
    this.loadModels();
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
