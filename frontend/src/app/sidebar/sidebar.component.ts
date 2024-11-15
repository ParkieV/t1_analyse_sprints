import { Component } from '@angular/core';
import { SidebarLinkComponent } from './sidebar-link/sidebar-link.component';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [SidebarLinkComponent],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {

}
