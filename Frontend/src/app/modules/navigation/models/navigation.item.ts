import { Signal } from '@angular/core';

export class NavigationItem {
  Icon?: string;
  svgIcon?: string;
  Name?: string;
  RoutingPath?: string;
  BadgeValue?: string;
  HideBadge?: Signal<boolean> | undefined = undefined;
}
