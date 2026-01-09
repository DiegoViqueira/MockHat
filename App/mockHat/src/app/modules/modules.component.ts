import { Component, inject, OnInit, Signal } from '@angular/core';
import { SessionService } from '../@core/auth/services/session.service';
import { User } from '../@core/auth/models/users';

@Component({
  selector: 'app-modules',
  templateUrl: './modules.component.html',
  styleUrls: ['./modules.component.scss'],
})
export class ModulesComponent implements OnInit {
  user: Signal<User | null>;



  public appPages = [
    { title: 'wirting', url: '/modules/writing', icon: 'pencil' },
    { title: 'grammar', url: '/modules/grammar', icon: 'language' },
  ];
  constructor(session: SessionService) {
    this.user = session.user;
  }

  ngOnInit() { }

}
