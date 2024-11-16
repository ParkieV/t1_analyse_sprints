import { Component } from '@angular/core';
import { SprintHeaderComponent } from "./sprint-header/sprint-header.component";

@Component({
  selector: 'app-sprint-detail',
  standalone: true,
  imports: [SprintHeaderComponent],
  templateUrl: './sprint-detail.component.html',
  styleUrl: './sprint-detail.component.scss'
})
export class SprintDetailComponent {

}
