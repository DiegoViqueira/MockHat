import { Component, computed, effect, inject, signal } from '@angular/core';
import { ClassStore } from '../../stores/class.store';
import { canMatchAdminRoleGuard } from '../../../../@core/auth/guards/canMatchRoleGuard';
import { MatDialog } from '@angular/material/dialog';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { ActivatedRoute, Router } from '@angular/router';
import { AssessmentStore } from '../../../assessments/stores/assessment.store';
import { Assessment } from '../../../assessments/models/assessment.model';
import { Role } from '../../../../@core/auth/models/role.enum';
import { UserStore } from '../../../users/stores/user.store';
import { DeleteTemplateComponent } from '../../../../@shared/components/delete-dialog/delete-template.component';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
@Component({
  selector: 'wlk-class-item',
  templateUrl: './class-item.component.html',
  styleUrl: './class-item.component.scss',
  standalone: false
})
export class ClassItemComponent {
  isAdmin = canMatchAdminRoleGuard();
  store = inject(ClassStore);
  dialog = inject(MatDialog);
  userStore = inject(UserStore);
  router = inject(Router);
  route = inject(ActivatedRoute);
  class = computed(() => this.store.class());
  user = computed(() => this.userStore.user());
  assessmentStore = inject(AssessmentStore);
  assessments = computed(() => this.assessmentStore.assessments());

  isActive = signal(this.class()?.is_active);


  // Definir las columnas que se mostrarán
  displayedColumns: string[] = ['title', 'state', 'actions'];

  toAssessments = false;
  constructor() {

    effect(() => {
      if (this.class()) {
        this.loadAssessments();
        this.isActive.set(this.class()?.is_active);
      }
    });
  }

  onToggleClass(event: MatSlideToggleChange) {

    const previousState = this.isActive();
    //are you sure?
    const dialogRef = this.dialog.open(DeleteTemplateComponent, {
      data: {
        title: 'common.are_you_sure',
        message: 'common.are_you_sure_message'
      }
    });

    dialogRef.afterClosed().subscribe((result: boolean) => {
      if (result) {
        this.store.update({ ...this.class(), is_active: !this.class().is_active });
      }
      else {
        event.source.checked = previousState;
      }
    });

  }


  onTabChange(event: any) {
    //console.log(event.index);
  }

  ngOnInit() {
    this.toAssessments = this.route.snapshot.queryParams['to'] === 'assessments';
    this.route.queryParams = null;
  }


  toUrl = {
    route: [AppRoutes.Modules, AppRoutes.Classes]
  };



  navigateToViewAssessment(assessment: Assessment) {
    this.assessmentStore.setAssessment(assessment);
    this.router.navigate([AppRoutes.Modules, AppRoutes.Assessments, AppRoutes.ViewAssessment],
      {
        queryParams: { mode: 'view' }
      }
    );
  }

  navigateToCorrectAssessment(assessment: Assessment) {
    this.assessmentStore.setAssessment(assessment);
    this.router.navigate([AppRoutes.Modules, AppRoutes.Assessments, AppRoutes.ViewAssessment],
      {
        queryParams: { mode: 'correct' }
      }
    );
  }

  isMember(role: Role) {
    return role === Role.MEMBER;
  }

  navigateToCreateAssessment() {
    this.router.navigate([AppRoutes.Modules, AppRoutes.Assessments, AppRoutes.CreateAssessment]);
  }



  loadAssessments() {
    this.assessmentStore.loadByClassId(this.class()._id);
  }
}
