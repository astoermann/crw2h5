# YAML Files

YAML is a human readable markup language with easy file structures to quickly create documents that are easily imported to other languages. 

For more information on YAML language: [YAML documentation](https://yaml.org/spec/1.2/spec.html)


## YAML Header

The YAML header (yhdr) is an open-ended mechanism for storing extra information with the EEG data that are useful for record keeping or subsequent data analysis. For instance
* recording session information:
* subject variables, e.g., DOB, meds, neuropsych scores
* instrument settings, e.g., bioamp gain and filter, electrode locations

Like other Linux files, `#` &nbsp; can be used to add comments for yourself that you don't actually want in the data

yhdr specification:
* Must conform to YAML syntax (can use the Linux command `yamllint` to check for errors
* Must contain at least one YAML document, may contain more.
* Each YAML document must contain the key name and a string label for a value, and may contain more keys with values.


Minimal requirements for a yhdr:

```{admonition} Simple Example
	## A minimal, yet legal yhdr file
	---
	name: pointless_yhdr
```

A more realistic example:

```{admonition} Simple Example
	# stmath yhdr file
	--- 
	name: runsheet
	subid: stm02
	experiment: stmath
	experimenter: Anna
	hand: right
```

## YAML Header Extractor

If you are putting information in your yhdr beyond the simple example that you are not planning on merging in some other way, you will need to create a YAML header extraxtor (yhdx) file

For each key/value pair you want to extract, you will write what you would like the key to extract as in your database. This does not have to be for every line in your yhdr, and the names for the database can either be the same or different from the key names. 

This document has the same specifications as the yhdr above. In addition, the syntax for naming the columns is\
`key: column name`

```{admonition} Example
	# stmath yhdx file
	--- 
	name: runsheet

	experimenter: experimenter
	hand: handedness
```
