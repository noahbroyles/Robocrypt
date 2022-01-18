package db;

import dict.Dictionary;


public class Row {
	
	private Dictionary data;
	
	public Row(Dictionary dict) {
		this.data = dict;
	}
	
	public Object get(String key) {
		return this.data.get(key);
	}
	
	public Dictionary toDict() {
		return new Dictionary(this.data);
	}
	
	public String toString() {
		return this.data.toString();
	}
}