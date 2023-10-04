import NodeCache from 'node-cache';

export class Cache extends NodeCache {
  constructor() {
    super({
        stdTTL: 1 * 60 * 1, 
        checkperiod: 1 * 60 * 1
    });    
  }

  public add( key: string) : void {
    console.log("add cache")
  }
}
