import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { AppRoutes } from '../../../../@core/auth/models/routes.enum';
import { NavigationError, Router } from '@angular/router';
import { ClassCreateComponent } from '../../components/class-create/class-create.component';
import { MatDialog } from '@angular/material/dialog';
import { Class } from '../../models/class.model';
import { ClassStore } from '../../stores/class.store';
import { canMatchAdminRoleGuard } from '../../../../@core/auth/guards/canMatchRoleGuard';
import { AssessmentPollingService } from '../../../assessments/services/assessment-polling.service';


@Component({
  selector: 'wlk-classes-management',
  templateUrl: './classes-management.component.html',
  styleUrl: './classes-management.component.scss',
  standalone: false,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ClassesManagementComponent {


  store = inject(ClassStore);
  router = inject(Router);
  active = signal(true);
  dialog = inject(MatDialog);
  isAdmin = canMatchAdminRoleGuard();

  private assessmentPollingService: AssessmentPollingService = inject(AssessmentPollingService);


  ngOnInit() {

    this.router.events.subscribe(event => {
      if (event instanceof NavigationError) {
        console.error('Error de navegación:', event.error);
      }
    });

    this.store.loadByQuery({ limit: 10000, offset: 0, isActive: true, search: undefined });

  }

  createClass() {
    const dialogRef = this.dialog.open(ClassCreateComponent, {
      data: {},
      width: '50%',
      height: 'auto'
    });
    dialogRef.afterClosed().subscribe(result => {

      if (result !== undefined) {
        this.store.create(result as Class);
      }
    });
  }

  goToClass(classItem: Class) {

    this.store.setClass(classItem);
    this.router.navigate([AppRoutes.Modules, AppRoutes.Classes, AppRoutes.Class]);
  }

  viewMetrics(classItem: Class) {
    this.store.setClass(classItem);
    this.router.navigate([AppRoutes.Modules, AppRoutes.Classes, AppRoutes.ClassMetrics]);
  }

  viewClassAnalysis(classItem: Class) {
    this.store.setClass(classItem);
    this.router.navigate([AppRoutes.Modules, AppRoutes.Classes, AppRoutes.ClassAnalysis]);
  }



  onTabChange(event: any) {

    if (event.index === 0) {
      this.activeClasses();
    } else {
      this.inactiveClasses();
    }
  }

  activeClasses() {
    this.active.set(true);
    this.store.loadByQuery({ limit: 10000, offset: 0, isActive: true, search: undefined });
  }

  inactiveClasses() {
    this.active.set(false);
    this.store.loadByQuery({ limit: 10000, offset: 0, isActive: false, search: undefined });
  }

}
