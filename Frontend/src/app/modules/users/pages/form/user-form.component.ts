import { Component, EventEmitter, Input, OnChanges, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { User } from '../../models/user.model';
import { Role } from '../../../../@core/auth/models/role.enum';

@Component({
  selector: 'hrt-user-form',
  templateUrl: './user-form.component.html',
  standalone: false
})
export class UserFormComponent implements OnChanges {
  @Input() user: User | null = null;
  @Output() save: EventEmitter<User> = new EventEmitter<User>();
  @Output() back: EventEmitter<void> = new EventEmitter();
  userRoles = [Role.ADMIN, Role.MEMBER];

  private minUsername = 3;
  formUser: FormGroup = this.fb.nonNullable.group({
    _id: undefined,
    account_id: undefined,
    email: ['', [Validators.required, Validators.email]],
    first_name: ['', [Validators.required, Validators.minLength(this.minUsername)]],
    last_name: ['', [Validators.required, Validators.minLength(this.minUsername)]],
    role: Role.MEMBER,
    disabled: false,
    verified: false,
    created_at: new Date(),
    updated_at: new Date(),
  });

  constructor(private fb: FormBuilder) { }

  get email() {
    return this.formUser.controls.email;
  }

  onCancel() {
    this.back.emit();
  }

  onSubmit() {
    this.save.emit(this.formUser.getRawValue());
  }

  ngOnChanges(): void {
    if (this.user !== null) {
      this.formUser.setValue(this.user);
    }
  }
}
