import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'sims-taxa-event-list',
  templateUrl: './taxa-event-list.component.html',
  styleUrls: ['./taxa-event-list.component.scss']
})
export class TaxaEventListComponent implements OnInit {

  taxaId: string;
  
  filter: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.taxaId = pmap.get('taxaId');
    });
    this.filter = 'taxa:' + this.taxaId;
  }
}
