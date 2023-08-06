# Example Package

Date Extraction library built on top of Python native date libraries to support business vocabularies.

# Installation
	` pip install datelibrary-javis`

#Usage
	`import datelibrary
	 from datelibrary.dates import DateData

	 text = "my sales from june to sept'

	 date_obj = DateData(text)

	 print(date_obj.comile_dates())

	 >>>

	 `

# Scope

	current date = 5th November 2019
	| Type | Parsed Date |
	| --- | --- |
	| ytd | [] |
	