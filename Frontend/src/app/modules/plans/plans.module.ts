import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule, NgOptimizedImage } from '@angular/common';
import { PlanInfoComponent } from './pages/plan-info/plan-info.component';
import { PlansComponent } from './plans.component';
import { SharedModule } from '../../@shared/shared.module';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatDialogModule } from '@angular/material/dialog';
import { MatMenuModule } from '@angular/material/menu';
import { MatPaginator } from '@angular/material/paginator';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatCheckbox } from '@angular/material/checkbox';
import { MatDatepicker, MatDatepickerToggle } from '@angular/material/datepicker';
import {
  MatChipGrid,
  MatChipInput,
  MatChipRemove,
  MatChipRow,
  MatChipsModule,
} from '@angular/material/chips';
import { MatStepperModule } from '@angular/material/stepper';
import { PlansRoutingModule } from './plans-routing.module';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatListModule } from '@angular/material/list';

@NgModule({
  declarations: [PlansComponent, PlanInfoComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  imports: [
    CommonModule,
    PlansRoutingModule,
    SharedModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatInputModule,
    MatDialogModule,
    MatMenuModule,
    MatPaginator,
    MatSelectModule,
    MatTableModule,
    MatTooltipModule,
    MatCheckbox,
    MatDatepickerToggle,
    MatDatepicker,
    MatChipGrid,
    MatChipRow,
    MatChipInput,
    MatChipRemove,
    MatChipsModule,
    NgOptimizedImage,
    MatStepperModule,
    MatListModule,
    MatGridListModule,
  ],
  exports: [PlansComponent, PlanInfoComponent],
})
export class PlansModule {}
