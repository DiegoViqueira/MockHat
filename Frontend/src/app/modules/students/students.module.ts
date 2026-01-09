import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StudentsComponent } from './pages/students/students.component';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatCardModule } from '@angular/material/card';
import { StudentDialogComponent } from './components/student-dialog.component';
import { ReactiveFormsModule } from '@angular/forms';
import { MAT_FORM_FIELD_DEFAULT_OPTIONS, MatFormFieldModule } from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { MatButtonModule, MatMiniFabButton } from '@angular/material/button';
import { MatTooltip } from '@angular/material/tooltip';
import { TranslateModule } from '@ngx-translate/core';
import { MatSelectModule } from '@angular/material/select';
import { MatInputModule } from '@angular/material/input';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatChipsModule } from '@angular/material/chips';
import { StudentsRoutingModule } from './students-routing.module';
import { MatSortModule } from '@angular/material/sort';
import { SharedModule } from '../../@shared/shared.module';
@NgModule({
  declarations: [StudentsComponent, StudentDialogComponent],
  exports: [StudentsComponent, StudentDialogComponent],
  imports: [
    CommonModule,
    StudentsRoutingModule,
    MatTableModule,
    MatPaginatorModule,
    MatCardModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatIcon,
    MatMiniFabButton,
    MatTooltip,
    TranslateModule,
    MatSelectModule,
    MatButtonModule,
    MatInputModule,
    MatSlideToggleModule,
    MatChipsModule,
    MatPaginatorModule,
    MatSortModule,
    SharedModule,
  ],
  providers: [
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: { appearance: 'fill' },
    },
  ],
})
export class StudentsModule { }
