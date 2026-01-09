import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Institution } from '../../../shared/models/institutions.enum';
import { Level } from '../../../users/models/user-level.enum';
import { getLevelsByInstitution, institutions } from '../../../../@shared/common-environment/common-environment';

@Component({
  selector: 'wlk-class-create',
  templateUrl: './class-create.component.html',
  styleUrl: './class-create.component.scss',
  standalone: false,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ClassCreateComponent {

  data = inject(MAT_DIALOG_DATA);
  formBuilder = inject(FormBuilder);
  form!: FormGroup;
  availableLevels: Level[] = [];
  institutions = institutions;
  dialogRef = inject(MatDialogRef);
  constructor(

  ) {
    this.form = this.formBuilder.group({
      name: ['', [Validators.required]],
      description: [''],
      institution: [Institution.CAMBRIDGE, [Validators.required]],
      level: [Level.B1, [Validators.required]],
    });

    this.availableLevels = getLevelsByInstitution(Institution.CAMBRIDGE);
  }

  onInstitutionChange(institution: Institution) {
    this.form.get('institution')?.setValue(institution);
    this.availableLevels = getLevelsByInstitution(institution);
  }

  onSubmit() {
    if (this.form.valid) {
      this.dialogRef.close(this.form.getRawValue());
    }
  }

  close(): void {
    this.dialogRef.close(undefined);
  }

}
