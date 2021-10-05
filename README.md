<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
  <h2>Elite Dangerous Wing Massacre Mission</h2>

  <p>
    Lately it has become very hard to find a good system
    to do Bounty Hunting in Elite Dangerous, Maybe the reason
    is with Player factions pushing system in War or
    it Frontier Developers becoming insane.
    Its just like the NPC crew member, more increase in rank make
    them more stupid.
  </p>
  
<h3> Purpose of this Script</h3>
  <p>
    This script would filter out systems
    are in any type of Conflict.
  
    *More states would be added later.
  </p>

<h3>Installation</h3>
<div>
  <ul>
    <li>Install Python 3.7+ from <a href="https://www.python.org/downloads/">Python.org</a></li>
    <li>While installing add Python to your path, it would ask you during installation, probably at the beginning</li>
    <li>Open Powershell or Command Prompt and copy & paste following
      
    python -m pip install bs4 pandas lxml
</li>
  </ul>
</div>

<div>
  <h3>Process to find Systems</h3>
  <ul>
    <li>Download as zip or Clone this project, extract it, open this folder, press and hold shift key 
      while right mouse or touchpad click (Windows 10) or Simple right click on Windows 11.</li>
    <li>Click on "Open Powershell window here" in windows 10 or "Open in Windows Terminal" in Windows 11.</li>
    <li>Run

    python main.py #arguments here
  </li>
    <li>Example to search a system with following arguments.<br>
      * Least No of Federation Faction (--fed) = 2 <br>
      * Least No of Imperial Faction (--imp) = 1 <br>
      * Least No of Alliance Faction (--all) = 1 <br>
      * Least No of Independent Faction (--ind) = 2 <br>
      * Reference System = "Sol" (--ref) <br>
      * Distance in Light Years from Reference System (--dist) = 100<br>
      * Resource Extraction Site = "Hazardous Site" insort "haz" <br>
        
    python main.py --fed 2 --imp 1 --all 1 --ind 1 --ref "Sol" --res "haz" --dist 100
  </li>
    <li>Note: if any of of faction is omitted would be considered greater then 0<br>
      Reference system: "Sol"<br>
      Distance: 20 Ly<br>
      Resource Extraction Site: "any"<br>
        **Order of these arguments does not matter.**
    </li>
  </ul>

  <h5>Final Result would be stored in an HTML file name as Final_Result.html</h5>
</div>

</body>
</html>
