import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ClassesRoutingModule } from './classes-routing.module';
import { ClassesManagementComponent } from './pages/classes/classes-management.component';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialogModule } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { TranslateModule } from '@ngx-translate/core';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { ClassItemComponent } from './pages/class-item/class-item.component';
import { RouterModule, RouterOutlet } from '@angular/router';
import { ClassesComponent } from './classes.component';
import { ClassCreateComponent } from './components/class-create/class-create.component';
import { ReactiveFormsModule } from '@angular/forms';
import { OverlayModule } from '@angular/cdk/overlay';
import { SharedModule } from '../../@shared/shared.module';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatChipsModule } from '@angular/material/chips';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatTableModule } from '@angular/material/table';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSortModule } from '@angular/material/sort';
import { ClassesTableComponent } from './components/classes-table/classes-table.component';
import { MatTabsModule } from '@angular/material/tabs';
import { MatPaginatorModule } from '@angular/material/paginator';
import { ClassAssessmentsTableComponent } from './components/class-assessments-table/class-assessments-table.component';
import { ClassMembersTableComponent } from './components/class-members-table/class-members-table.component';
import { AddMemberToClassComponent } from './components/add-member-to-class/add-member-to-class.component';
import { AddTeacherToClassComponent } from './components/add-teacher-to-class/add-teacher-to-class.component';
import { AddStudentToClassComponent } from './components/add-student-to-class/add-student-to-class.component';
import { MatListModule } from '@angular/material/list';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatMenuModule } from '@angular/material/menu';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { ClassMetricsComponent } from './pages/class-metrics/class-metrics.component';
import { ClassAnalisysComponent } from './components/class-analisys/class-analisys.component';
import { MarkdownModule } from 'ngx-markdown';
import { StudentsAnalysisTableComponent } from './components/students-analysis-table/students-analysis-table.component';
@NgModule({
  declarations: [
    ClassesComponent,
    ClassesManagementComponent,
    ClassItemComponent,
    ClassCreateComponent,
    ClassesTableComponent,
    ClassAssessmentsTableComponent,
    ClassMembersTableComponent,
    AddMemberToClassComponent,
    AddStudentToClassComponent,
    AddTeacherToClassComponent,
    ClassMetricsComponent,
    ClassAnalisysComponent,
    StudentsAnalysisTableComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    RouterOutlet,
    ClassesRoutingModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatTooltipModule,
    MatDialogModule,
    MatInputModule,
    TranslateModule,
    MatButtonToggleModule,
    ReactiveFormsModule,
    OverlayModule,
    SharedModule,
    MatSelectModule,
    MatFormFieldModule,
    MatChipsModule,
    MatAutocompleteModule,
    MatTableModule,
    MatToolbarModule,
    MatSortModule,
    MatTabsModule,
    MatPaginatorModule,
    MatListModule,
    MatCheckboxModule,
    MatMenuModule,
    MatSlideToggleModule,
    MarkdownModule.forChild()
  ],
  exports: [
    ClassesComponent,
    ClassesManagementComponent,
    ClassItemComponent,
    ClassCreateComponent,
    ClassesTableComponent,
    ClassAssessmentsTableComponent,
    ClassMembersTableComponent,
    AddMemberToClassComponent,
    AddStudentToClassComponent,
    AddTeacherToClassComponent,
    ClassMetricsComponent,
    ClassAnalisysComponent,
    StudentsAnalysisTableComponent
  ]
})
export class ClassesModule { }
