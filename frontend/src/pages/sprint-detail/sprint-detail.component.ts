import { Component } from '@angular/core';
import { SprintHeaderComponent } from "./sprint-header/sprint-header.component";
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-sprint-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, SprintHeaderComponent],
  templateUrl: './sprint-detail.component.html',
  styleUrl: './sprint-detail.component.scss'
})
export class SprintDetailComponent {

}
