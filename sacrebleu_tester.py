from sacrebleu import corpus_bleu

original = """
BULLETIN - IMMEDIATE BROADCAST REQUESTED
Backcountry Avalanche Warning
Forest Service Utah Avalanche Center Salt Lake City UT
Relayed by National Weather Service Salt Lake City UT
641 AM MST Sun Feb 16 2025

...THE FOREST SERVICE UTAH AVALANCHE CENTER HAS CONTINUED A 
BACKCOUNTRY AVALANCHE WARNING WHICH IS IN EFFECT FROM 6 AM MST 
SUNDAY TO 6 AM MST MONDAY...

* WHAT..The avalanche danger for the warning area is HIGH. 

* WHERE...For most of the mountains of Utah, including the 
  Wasatch Range, uinta Mountains, Wasatch Plateau, Manti Skyline, 
  the Abajos, and the Tushar Range. 

* WHEN...In effect from 6am MST this morning to 6am MST Monday. 

* IMPACTS...Heavy snow and drifting by strong winds have created
  widespread areas of unstable snow and very dangerous avalanche
  conditions at all elevations. Natural and human-triggered
  avalanches are certain. People should avoid travel in all
  avalanche terrain and keep out of avalanche runouts. Avoid being
  on or under terrain steeper than 30 degrees. 

PRECAUTIONARY/PREPAREDNESS ACTIONS...

Stay off of and out from under slopes steeper than 30 degrees.

Backcountry travelers should consult www.utahavalanchecenter.org
or call 1-888-999-4019 for more detailed information. 

This Warning does not apply to ski areas where avalanche hazard
reduction measures are performed.

$$"""

azure = """
Bulletin Board - Request an instant broadcast
Remote avalanche warning
Forest Service Utah Avalanche Center Salt Lake City Utah
Broadcast by the National Weather Service, Salt Lake City, Utah
641 AM (MST) Sunday, February 16, 2025

... THE FOREST SERVICE UTAH AVALANCHE CENTER HAS CONTINUED TO DO THE FOLLOWING: 
A BACKCOUNTRY AVALANCHE WARNING IS IN EFFECT AT 6 A.M. MST. 
Sunday to Monday 6 a.m. MST...

*What.. The avalanche risk in the warning area is high. 

*Where is... Most of Utah's mountains, including 
  Wasatch Mountains, Yuinta Mountains, Wasatch Plateau, Manti Skyline, 
  Abajos and Tushar Range. 

*When... Valid from 6 a.m. MST this morning to 6 a.m. MST Monday. 

*Influence... Drifting caused by heavy snow and strong winds created.
  Unstable snow and very dangerous avalanches are widespread.
  All altitude conditions. It is natural and caused by humans.
  The avalanche is for sure. People should avoid traveling everywhere.
  Avoid avalanche terrain and avalanche runouts. Avoid
  Above or below terrain steeper than 30 degrees. 

Preventive/preparedness measures...

Take off slopes steeper than 30 degrees.

Backcountry travelers should www.utahavalanchecenter.org
Or call 1-888-999-4019 for more information. 

This warning does not apply to ski resorts with avalanche hazards.
Abatement measures are carried out.

$$"""

google = """Bulletin Board - Request for immediate broadcast
Backcountry Avalanche Warning
Forest Service Utah Avalanche Center Salt Lake City UT
Reported by National Weather Service Salt Lake City UT
Sunday, February 16, 2025 6:41 AM MST

...the Utah Forest Service Avalanche Center remained open. 
Backcountry Avalanche Warning in effect from 6 a.m. MST 
Sunday through Monday at 6am MST...

* Avalanche risk is high in the warning zone. 

* Location...including most of Utah's mountains 
  Wasatch Mountains, Uinta Mountains, Wasatch Plateau, Manti Skyline, 
  The Avajo Mountains and the Tushar Mountains. 

* When...Applies from 6:00 AM MST today through 6:00 AM MST Monday. 

* Impact...Drift occurred due to heavy snow and strong winds.
  Widespread unstable snow cover and extremely dangerous avalanches
  Natural or artificial conditions at all altitudes
  Avalanches are a certainty. People should avoid traveling in all areas.
  Avoid terrain prone to avalanches and avoid avalanche hotspots.
  On or below terrain steeper than 30 degrees. 

Preventive/Preventive Measures...

Stay away from slopes with an incline greater than 30 degrees.

Those traveling into the wilderness should visit www.utahavalanchecenter.org.
For more information, please call 1-888-999-4019. 

This warning does not apply to ski areas with avalanche hazards.
Reduction measures are implemented.

$$"""

copy = """ 
BULLETIN - IMMEDIATE BROADCAST REQUESTED
Backcountry Avalanche Warning
Forest Service Utah Avalanche Center Salt Lake City UT
Relayed by National Weather Service Salt Lake City UT
641 AM MST Sun Feb 16 2025

...THE FOREST SERVICE UTAH AVALANCHE CENTER HAS CONTINUED A 
BACKCOUNTRY AVALANCHE WARNING WHICH IS IN EFFECT FROM 6 AM MST 
SUNDAY TO 6 AM MST MONDAY...

* WHAT..The avalanche danger for the warning area is HIGH. 

* WHERE...For most of the mountains of Utah, including the 
  Wasatch Range, uinta Mountains, Wasatch Plateau, Manti Skyline, 
  the Abajos, and the Tushar Range. 

* WHEN...In effect from 6am MST this morning to 6am MST Monday. 

* IMPACTS...Heavy snow and drifting by strong winds have created
  widespread areas of unstable snow and very dangerous avalanche
  conditions at all elevations. Natural and human-triggered
  avalanches are certain. People should avoid travel in all
  avalanche terrain and keep out of avalanche runouts. Avoid being
  on or under terrain steeper than 30 degrees. 

PRECAUTIONARY/PREPAREDNESS ACTIONS...

Stay off of and out from under slopes steeper than 30 degrees.

Backcountry travelers should consult www.utahavalanchecenter.org
or call 1-888-999-4019 for more detailed information. 

This Warning does not apply to ski areas where avalanche hazard
reduction measures are performed.

$$"""

# Prepare data for BLEU calculation
reference = [original.strip()]
azure_bt = [azure.strip()]
google_bt = [google.strip()]
copy_bt = [copy.strip()]

# Compute BLEU scores
bleu_azure = corpus_bleu(azure_bt, [reference])
bleu_google = corpus_bleu(google_bt, [reference])
bleu_copy = corpus_bleu(copy_bt, [reference])

# Output results
print(f"BLEU (Azure):  {bleu_azure.score:.2f}")
print(f"BLEU (Google): {bleu_google.score:.2f}")
print(f"BLEU (Copy):   {bleu_copy.score:.2f}")
