import { Component, computed, effect, inject, signal } from '@angular/core';
import { StudentsStore } from '../../../students/stores/students.store';
import { ClassStore } from '../../stores/class.store';
import { DeviceDetectionService } from '../../../../@core/services/device-detection.service';
import { MatDialog } from '@angular/material/dialog';
import { StudentDialogComponent } from '../../../students/components/student-dialog.component';


export interface StudentItem {
  id: string;
  avatar: string;
  name: string;
  selected: boolean;
}

@Component({
  selector: 'wlk-add-student-to-class',
  templateUrl: './add-student-to-class.component.html',
  styleUrls: ['./add-student-to-class.component.scss'],
  standalone: false,
})
export class AddStudentToClassComponent {
  dialog = inject(MatDialog);
  store = inject(StudentsStore);
  students = computed(() => this.store.students());
  classStore = inject(ClassStore);
  class = computed(() => this.classStore.class());

  device = inject(DeviceDetectionService);
  isMobile = this.device.isMobileScreen;

  constructor() {
    effect(() => {
      this.filteredUsers.set(this.students().map(student => ({
        id: student._id,
        avatar: student.name.charAt(0) + student.last_name.charAt(0),
        name: student.name + ' ' + student.last_name,
        selected: false
      })));

      this.classStore.class().students.forEach(student => {
        this.filteredUsers.update(users => users.map(user => {
          if (user.id === student._id) {
            user.selected = true;
          }
          return user;
        }));
      });

    });
  }

  onSelectionChange(event) {
    const selectedUser = event.options[0].value;
    const isSelected = event.options[0].selected;

    if (isSelected) {
      const student = this.students().find(student => student._id === selectedUser.id);
      this.classStore.addStudentToClass(student);
    } else {
      const student = this.students().find(student => student._id === selectedUser.id);
      this.classStore.removeStudentFromClass(student);
    }

    this.filteredUsers.update(users => users.map(user => {
      if (user.id === selectedUser.id) {
        user.selected = isSelected;
      }
      return user;
    }));

  }

  filteredUsers = signal<StudentItem[]>([]);

  applyFilter(event: Event) {

    const filterValue = (event.target as HTMLInputElement).value;
    if (this.students()) {
      this.filteredUsers.set(this.students().filter(u =>
        u.name.toLowerCase().includes(filterValue.trim().toLowerCase())
      ).map(student => ({
        id: student._id,
        avatar: student.name.charAt(0) + student.last_name.charAt(0),
        name: student.name + ' ' + student.last_name,
        selected: this.class().students.some(s => s._id === student._id)
      })));
    }
  }

  addStudent() {
    this.dialog
      .open(StudentDialogComponent, {
        data: {
          student: undefined,
        },
      })
      .afterClosed()
      .subscribe((x) => {
        if (x) this.store.create(x);
      });
  }
}
