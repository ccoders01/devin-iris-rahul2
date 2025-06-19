import { Routes } from '@angular/router';
import { ModelRegistrationComponent } from './components/model-registration/model-registration.component';
import { ModelInventoryComponent } from './components/model-inventory/model-inventory.component';

export const routes: Routes = [
  { path: '', redirectTo: '/register', pathMatch: 'full' },
  { path: 'register', component: ModelRegistrationComponent },
  { path: 'inventory', component: ModelInventoryComponent },
  { path: '**', redirectTo: '/register' }
];
