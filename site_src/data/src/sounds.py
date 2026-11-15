import json,re
P='../species.json'; d=json.load(open(P))
C={ # curated: name keyword -> (description, commons query)
"Humpback whale":("Long, complex songs of moans, groans, whoops and cries lasting 10–20 minutes, sung by males and changing year to year; they spread across ocean basins like pop hits.","humpback whale song"),
"Blue whale":("Extremely loud, very low-frequency moans and pulses (mostly below 20 Hz, too low for humans to hear unsped). They can travel hundreds of kilometres.","blue whale call"),
"Fin whale":("Repetitive 20 Hz pulses, one of the most powerful sounds made by any animal, usually sped up so humans can hear them.","fin whale 20 Hz"),
"Sperm whale":("Loud clicks, the loudest sounds made by any animal (~230 dB), used for echolocation; patterned 'codas' work like clan dialects.","sperm whale clicks"),
"Orca":("Whistles, clicks and pulsed calls; each pod has its own dialect passed down through generations.","orca vocalization"),
"Beluga":("So chatty it's called the 'canary of the sea': chirps, whistles, squeals, clicks and bell-like tones.","beluga whale sound"),
"Bowhead":("Complex, jazz-like songs that change constantly through the winter breeding season.","bowhead whale song"),
"Bottlenose dolphin":("Rapid clicks for echolocation, burst pulses and signature whistles that act like individual names.","bottlenose dolphin whistle"),
"Walrus":("Bell-like knocks, whistles and grunts; males 'sing' underwater for days during the breeding season.","walrus vocalization"),
"Bearded seal":("Long, descending, spiralling trills underwater, among the most haunting sounds of the Arctic.","bearded seal song"),
"Weddell seal":("Eerie, otherworldly trills, chirps and whistles that sound almost electronic under the ice.","Weddell seal calls"),
"Leopard seal":("Low, droning songs and ultrasonic-like trills during the breeding season.","leopard seal call"),
"Snapping shrimp":("A loud crackle like frying bacon; colonies make so much noise they interfere with sonar.","snapping shrimp"),
"Bigclaw snapping shrimp":("A single sharp 'snap' as a cavitation bubble collapses, as loud as ~210 dB at close range.","snapping shrimp"),
"toadfish":("A low, foghorn-like 'boatwhistle' hum made by vibrating the swim bladder.","toadfish boatwhistle"),
"midshipman":("A continuous drone-like hum lasting up to an hour, once mistaken for machinery by houseboat owners.","plainfin midshipman hum"),
"drum":("Loud drumming and croaking made by muscles beating against the swim bladder, especially at spawning time.","drum fish sound"),
"croaker":("Croaking, knocking sounds from the swim bladder, loudest during spawning choruses.","Atlantic croaker sound"),
"grunt":("Grunting sounds made by grinding the pharyngeal (throat) teeth, amplified by the swim bladder.","grunt fish sound"),
"Goliath grouper":("Deep booming sounds felt as much as heard, used to warn intruders.","goliath grouper boom"),
"grouper":("Low booms and grunts from the swim bladder, especially at spawning aggregations.","grouper sound"),
"squirrelfish":("Clicking, grunting and staccato sounds when threatened.","squirrelfish sound"),
"piranha":("Barks, drums and croaks when threatened or fighting.","piranha sound"),
"gurnard":("Grunts and croaks produced by the swim bladder.","gurnard sound"),
"clownfish":("Popping and clicking sounds made by snapping the jaw, used to defend the anemone and set rank.","clownfish sound"),
"anemonefish":("Pops and chirps made with the jaw, used in disputes over rank.","clownfish sound"),
"Atlantic cod":("Low grunts made by the swim bladder during spawning.","cod grunting"),
"haddock":("Knocking sounds that speed up into a continuous hum during courtship.","haddock sound"),
"herring":("High-pitched 'fast repetitive tick' bursts released as bubbles from the anus, possibly used at night to keep schools together.","herring sound"),
"Atlantic puffin":("A deep, growling purr at the burrow, sounding like a distant chainsaw.","Atlantic puffin call"),
"Northern gannet":("Harsh, guttural 'arrah-arrah' calls at crowded colonies.","northern gannet call"),
"penguin":("Loud trumpeting and braying calls; each bird recognises its partner's voice among thousands.","penguin call"),
"African penguin":("A donkey-like bray, which earned it the name 'jackass penguin'.","African penguin bray"),
"albatross":("Bill-clacking, whistles and sky-calls during elaborate courtship dances.","albatross call"),
"tern":("Sharp, grating 'kee-arr' calls, loud in nesting colonies.","tern call"),
"gull":("Loud laughing, mewing and long-calls.","gull call"),
"kittiwake":("Calls its own name, 'kitti-waake', at cliff colonies.","kittiwake call"),
"shearwater":("Eerie wailing and cackling at night over nesting burrows; once thought to be ghosts.","Manx shearwater"),
"Osprey":("High-pitched whistled chirps.","osprey call"),
"Ganges river dolphin":("Nearly continuous echolocation clicks, since it is almost blind in muddy water.","Ganges river dolphin clicks"),
"manatee":("Squeaks and chirps, especially between mothers and calves.","manatee vocalization"),
"Sea otter":("Squeals, whistles and screams, especially from pups.","sea otter vocalization"),
"alligator":("Deep bellows that make the water dance on their backs.","American alligator bellow"),
"crocodile":("Hatchlings chirp from inside the egg; adults roar, hiss and bellow.","crocodile sound"),
"sea lion":("Loud barking, honking and roaring at haul-outs.","sea lion bark"),
"fur seal":("Barks, growls and high-pitched pup calls.","fur seal"),
"elephant seal":("Males make deep, drum-like clap-threats; each has a recognisable rhythm.","elephant seal"),
"Spiny lobster":("A rasping 'stridulation' made by rubbing an antenna base, like a violin bow, to startle predators.","spiny lobster sound"),
"Caribbean spiny lobster":("A rasping stridulation sound used to startle predators.","spiny lobster sound"),
"mantis shrimp":("Low-frequency rumbles used to claim burrows, plus the crack of its strike.","mantis shrimp sound"),
"dolphin":("Rapid echolocation clicks, buzzes and whistles used to hunt and keep in touch.","dolphin whistle"),
"porpoise":("High-frequency clicks, mostly above human hearing; porpoises do not whistle.","porpoise click"),
"beaked whale":("Ultrasonic clicks and buzzes during deep foraging dives, rarely heard at the surface.","beaked whale click"),
"pilot whale":("Whistles and pulsed calls used to keep tight family groups together.","pilot whale"),
"right whale":("Rising 'up-calls' used as contact calls, plus loud 'gunshot' sounds.","right whale upcall"),
"minke":("Odd mechanical-sounding 'boings' (North Pacific) and 'bio-duck' quacks (Antarctic).","minke whale boing"),
"grey whale":("Low knocks, grunts and moans.","gray whale sound"),
"seal":("Barks, growls, grunts and underwater trills, especially in the breeding season.","seal vocalization"),
"otter":("Squeaks, chirps and whistles to keep family groups in contact.","otter vocalization"),
"sea urchin":("Feeding urchins scrape rocks, adding to the 'evening chorus' of reefs.","sea urchin sound"),
}
fam_vocal={"Marine mammals":"Vocal animal: produces calls underwater or in air, used for communication.","Seabirds":"Calls loudly at breeding colonies; mostly quiet at sea."}
n_cur=n_rule=0
for x in d:
    nm=x['name']; key=None
    for k in sorted(C,key=len,reverse=True):
        if k.lower() in nm.lower(): key=k;break
    g=x['group']; x.pop('silent',None)
    if key:
        x['sound_desc'],q=C[key]; x.setdefault('sound',q); n_cur+=1; continue
    n_rule+=1
    if g in fam_vocal:
        x['sound_desc']=fam_vocal[g]+" No species-specific description has been written yet; the player tries to find a recording."
    elif g=="Plants & algae":
        x['silent']=True; x['sound_desc']="Plants, algae and microbes make no sounds. (Seagrass meadows do 'fizz' faintly as oxygen bubbles are released in sunlight.)" if 'grass' in nm.lower() or 'Posidonia' in nm or 'Zostera' in x.get('scientific','') else "Plants, algae and microbes make no sounds."
    elif g in ("Cnidarians","Comb jellies & others","Sponges & others","Echinoderms","Worms & vent fauna"):
        x['silent']=True; x['sound_desc']="Never heard: animals like this have no sound-producing organs and are not known to make calls. Their only sounds are incidental, like the faint scraping of feeding."
    elif g in ("Molluscs","Cephalopods"):
        x['silent']=True; x['sound_desc']="Silent: molluscs and cephalopods are not known to make vocal sounds. Squid and octopuses communicate visually, with colour and skin patterns, instead."
    elif g=="Crustaceans":
        x['sound_desc']="Many crustaceans make clicks, rasps or snaps by rubbing or snapping body parts, but this species has no well-documented sound. The player tries to find a recording."
    elif g in ("Sea turtles & reptiles",):
        x['sound_desc']="Mostly silent. Sea turtle hatchlings 'talk' with low chirps inside the nest, and adults can hiss or grunt."
    elif g in ("Sharks & rays",):
        x['silent']=True; x['sound_desc']="Never heard: sharks and rays have no swim bladder or vocal organs and are considered silent. (In 2025 rig sharks were reported making clicks, a first for any shark.)"
    elif g in ("Rivers & estuaries",):
        x['sound_desc']="Sounds vary: river dolphins click and whistle, crocodilians bellow, otters chatter; many river fish are silent. The player tries to find a recording."
    else: # fish groups
        x['sound_desc']="Like most fish, mostly silent to human ears; some fish grunt, knock or drum with their swim bladder, but no recording of this species has been published that we know of. The player tries to find one."
json.dump(d,open(P,'w'),ensure_ascii=False,indent=0)
print("curated",n_cur,"rule",n_rule, "silent",sum(1 for x in d if x.get('silent')))
