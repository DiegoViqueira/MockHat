import { Component, computed, effect, inject, signal } from '@angular/core';
import { ClassStore } from '../../stores/class.store';
import { UserStore } from '../../../users/stores/user.store';

export interface TeacherItem {
  id: string;
  avatar: string;
  name: string;
  selected: boolean;
}

@Component({
  selector: 'wlk-add-teacher-to-class',
  templateUrl: './add-teacher-to-class.component.html',
  styleUrls: ['./add-teacher-to-class.component.scss'],
  standalone: false,
})
export class AddTeacherToClassComponent {
  store = inject(UserStore);
  teachers = computed(() => this.store.users());
  classStore = inject(ClassStore);
  class = computed(() => this.classStore.class());


  constructor() {
    effect(() => {

      this.filteredUsers.set(this.teachers().map(teacher => ({
        id: teacher._id,
        avatar: teacher.first_name.charAt(0) + teacher.last_name.charAt(0),
        name: teacher.first_name + ' ' + teacher.last_name,
        selected: false
      })));


      this.classStore.class().teachers.forEach(teacher => {
        this.filteredUsers.update(users => users.map(user => {
          if (user.id === teacher._id) {
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
      const teacher = this.teachers().find(teacher => teacher._id === selectedUser.id);
      this.classStore.addTeacherToClass(teacher);
    } else {
      const teacher = this.teachers().find(teacher => teacher._id === selectedUser.id);
      this.classStore.removeTeacherFromClass(teacher);
    }

    this.filteredUsers.update(users => users.map(user => {
      if (user.id === selectedUser.id) {
        user.selected = isSelected;
      }
      return user;
    }));

  }

  filteredUsers = signal<TeacherItem[]>([]);

  applyFilter(event: Event) {

    const filterValue = (event.target as HTMLInputElement).value;
    if (this.teachers()) {
      this.filteredUsers.set(this.teachers().filter(u =>
        u.first_name.toLowerCase().includes(filterValue.trim().toLowerCase())
      ).map(teacher => ({
        id: teacher._id,
        avatar: teacher.first_name.charAt(0) + teacher.last_name.charAt(0),
        name: teacher.first_name + ' ' + teacher.last_name,
        selected: this.class().teachers.some(t => t._id === teacher._id)
      })));
    }
  }

}
