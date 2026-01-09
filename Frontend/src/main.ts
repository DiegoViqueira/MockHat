import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';

const loadingElement = document.querySelector('.spinner');

platformBrowserDynamic()
  .bootstrapModule(AppModule)
  .then(() => {
    return loadingElement?.classList.add('loaded');
  })
  // remove the loading element after the transition is complete to prevent swallowed clicks
  .then(() => setTimeout(() => loadingElement?.remove(), 1000))
  .catch(err => console.error(err));
