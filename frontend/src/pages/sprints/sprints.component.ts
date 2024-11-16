import { Component } from '@angular/core';
import { SprintsFiltersComponent } from "./sprints-filters/sprints-filters.component";
import { SprintsTableComponent } from "./sprints-table/sprints-table.component";

@Component({
  selector: 'app-sprints',
  standalone: true,
  imports: [SprintsFiltersComponent, SprintsTableComponent],
  templateUrl: './sprints.component.html',
  styleUrl: './sprints.component.scss'
})
export class SprintsComponent {

}
