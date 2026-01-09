import { Component } from '@angular/core';
import { SessionService } from '../@core/auth/services/session.service';

@Component({
  selector: 'hrt-modules',
  templateUrl: './modules.component.html',
  standalone: false
})
export class ModulesComponent {
  constructor(
    protected session: SessionService
  ) {
  }


}
