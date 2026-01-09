import { Component, computed, effect, inject, ViewChild } from '@angular/core';
import { ClassStore } from '../../stores/class.store';
import { MatTableDataSource } from '@angular/material/table';
import { Student } from '../../../students/models/student.model';
import { DeviceDetectionService } from '../../../../@core/services/device-detection.service';
import { AddMemberToClassComponent } from '../add-member-to-class/add-member-to-class.component';
import { MatDialog } from '@angular/material/dialog';
import { MatSort } from '@angular/material/sort';
import { canMatchAdminRoleGuard } from '../../../../@core/auth/guards/canMatchRoleGuard';


export interface Member {
  id: string;
  avatar: string;
  name: string;
  role: string;
}

@Component({
  selector: 'wlk-class-members-table',
  templateUrl: './class-members-table.component.html',
  styleUrl: './class-members-table.component.scss',
  standalone: false
})
export class ClassMembersTableComponent {

  store = inject(ClassStore);
  dialog = inject(MatDialog);
  class = computed(() => this.store.class());
  displayedColumns: string[] = ['avatar', 'name', 'role'];

  device = inject(DeviceDetectionService);
  isMobile = this.device.isMobileScreen;
  dataSource = new MatTableDataSource<Member>([]);

  isAdmin = canMatchAdminRoleGuard();

  @ViewChild(MatSort) set matSort(ms: MatSort) {
    this.dataSource.sort = ms;
  }

  constructor() {

    effect(() => {

      if (this.class()) {
        this.dataSource.data = this.class()?.students.map(student => ({
          id: student._id,
          avatar: student.name.charAt(0) + student.last_name.charAt(0),
          name: student.name + ' ' + student.last_name,
          role: 'role.student'
        })).concat(this.class()?.teachers.map(teacher => ({
          id: teacher._id,
          avatar: teacher.first_name.charAt(0) + teacher.last_name.charAt(0),
          name: teacher.first_name + ' ' + teacher.last_name,
          role: 'role.teacher'
        })));
      }
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }


  addMember() {

    this.dialog.open(AddMemberToClassComponent, {
      data: this.class(),
      width: '80%',
      height: '80%',
    }).afterClosed().subscribe((student: Student) => {
      if (student) {
        this.store.addStudentToClass(student);
      }
    });
  }

}
