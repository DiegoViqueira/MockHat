import { Component, inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'wlk-add-member-to-class',
  templateUrl: './add-member-to-class.component.html',
  styleUrl: './add-member-to-class.component.scss',
  standalone: false
})
export class AddMemberToClassComponent {

  data = inject(MAT_DIALOG_DATA);

}
