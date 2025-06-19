import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ModelService } from '../../services/model.service';
import { ModelRequest, EnumValues, EnumOption } from '../../models/model.interface';

@Component({
  selector: 'app-model-registration',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './model-registration.component.html',
  styleUrls: ['./model-registration.component.css']
})
export class ModelRegistrationComponent implements OnInit {
  registrationForm: FormGroup;
  enumValues: EnumValues | null = null;
  isSubmitting = false;
  successMessage = '';
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private modelService: ModelService,
    public router: Router
  ) {
    this.registrationForm = this.fb.group({
      modelName: ['', [Validators.required]],
      modelVersion: ['', [Validators.required]],
      modelSponsor: ['', [Validators.required]],
      businessLine: ['', [Validators.required]],
      modelType: ['', [Validators.required]],
      riskRating: ['', [Validators.required]],
      status: ['', [Validators.required]]
    });
  }

  ngOnInit(): void {
    this.loadEnumValues();
  }

  loadEnumValues(): void {
    this.modelService.getEnumValues().subscribe({
      next: (data) => {
        this.enumValues = data;
      },
      error: (error) => {
        console.error('Error loading enum values:', error);
        this.errorMessage = 'Failed to load form options. Please try again.';
      }
    });
  }

  onSubmit(): void {
    if (this.registrationForm.valid) {
      this.isSubmitting = true;
      this.errorMessage = '';
      this.successMessage = '';

      const modelRequest: ModelRequest = this.registrationForm.value;

      this.modelService.registerModel(modelRequest).subscribe({
        next: (response) => {
          this.isSubmitting = false;
          this.successMessage = `Model '${response.modelName} ${response.modelVersion}' successfully registered with ID: ${response.id}`;
          this.registrationForm.reset();
          
          setTimeout(() => {
            this.router.navigate(['/inventory']);
          }, 2000);
        },
        error: (error) => {
          this.isSubmitting = false;
          console.error('Error registering model:', error);
          this.errorMessage = 'Failed to register model. Please check your input and try again.';
        }
      });
    } else {
      this.markFormGroupTouched();
    }
  }

  private markFormGroupTouched(): void {
    Object.keys(this.registrationForm.controls).forEach(key => {
      const control = this.registrationForm.get(key);
      control?.markAsTouched();
    });
  }

  getFieldError(fieldName: string): string {
    const control = this.registrationForm.get(fieldName);
    if (control?.errors && control.touched) {
      if (control.errors['required']) {
        return `${this.getFieldDisplayName(fieldName)} is required`;
      }
    }
    return '';
  }

  private getFieldDisplayName(fieldName: string): string {
    const displayNames: { [key: string]: string } = {
      modelName: 'Model Name',
      modelVersion: 'Model Version',
      modelSponsor: 'Model Sponsor',
      businessLine: 'Business Line',
      modelType: 'Model Type',
      riskRating: 'Risk Rating',
      status: 'Status'
    };
    return displayNames[fieldName] || fieldName;
  }
}
