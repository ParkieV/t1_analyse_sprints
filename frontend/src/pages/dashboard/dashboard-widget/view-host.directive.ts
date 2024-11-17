import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[viewHost], [view-host]',
  standalone: true,
})
export class ViewHostDirective {
  constructor(public viewContainerRef: ViewContainerRef) {}
}
