package dict;

import java.util.ArrayList;


/***
 * This class is meant to model a dictionary structure similar to Python. It has a very much Python-inspired toString.
 * The only thing I wasn't able to do was figure out how to use square bracket syntax, e.g. dictionary["key"] = "value". 
 * @author nbroyles
 *
 */
public class Dictionary {
	
	
	private ArrayList<String> keys;
	private ArrayList<Object> values;
	
	/*  Constructors  */
	public Dictionary() {
		this.keys = new ArrayList<String>();
		this.values = new ArrayList<Object>();
	}
	
	public Dictionary(ArrayList<String> keys, ArrayList<Object> values) {
		this.keys = keys;
		this.values = values;
		this.keys = new ArrayList<String>();
		this.values = new ArrayList<Object>();
	}
	
	public Dictionary(Dictionary d) {
		this.keys = d.keys;
		this.values = d.values;
	}
	
	
	/* Object Methods */
	public Object get(String key) {
		int index = this.keys.indexOf(key);
		if (index == -1) {
			// It's not found in the list of keys
			return false;
		} else {
			// It is in the list of keys
			return this.values.get(index);
		}
	}
	/***
	 * Returns the value at a certain index of the dictionary
	 * @param index
	 * @return Object
	 */
	public Object get(int index) {
		return this.values.get(index);
	}
	
	public void set(String key, Object value) {
		int index = this.keys.indexOf(key);
		if (index == -1) {
			// It's not found in the list of keys
			this.keys.add(key);
			this.values.add(value);
		} else {
			// It is in the list of keys
			// This is not good. It should not be here.
			this.values.set(index, value);
		}
	}
	
	public void remove(String key) {
		int index = this.keys.indexOf(key);
		try {
			this.keys.remove(index);
			this.values.remove(index);
		} catch (java.lang.IndexOutOfBoundsException ex) {
			System.err.println("KeyError: '" + key + "' does not exist");
		}
	}
	
	public Object pop(String key) {
		int index = this.keys.indexOf(key);
		Object val = null;
		try {
			this.keys.remove(index);
			val = this.values.get(index);
			this.values.remove(index);
			return val;
		} catch (java.lang.IndexOutOfBoundsException ex) {
			System.err.println("KeyError: '" + key + "' does not exist");
			return val;
		}
	}
	
	public int length() {
		return this.keys.size();
	}
	
	public ArrayList<String> keys() {
		return this.keys;
	}
	
	public ArrayList<Object> values() {
		return this.values;
	}
	
	// To String
	/***
	 * Returns a string representation of the dictionary
	 */
	public String toString() {
		String stringRep = "{";
		for (int i = 0; i < this.keys.size(); i++) {
			stringRep += "\"" + this.keys.get(i) + "\"" + ": ";
			
			// Account for NULL objects
			if (this.values.get(i) == null) {
				stringRep += "NULL";
			} else {
				if (this.values.get(i).getClass().getName() == "java.lang.String") {
					stringRep += "\"" + this.values.get(i) + "\"";
				} else {
					stringRep += this.values.get(i).toString();
				}
			}
			
			// Check to see if we should put a comma, basically if there is one after this.
			if (i < this.keys.size() - 1) {
				stringRep += ", ";
			}
		}
		stringRep += "}";
		return stringRep;
	}

}
