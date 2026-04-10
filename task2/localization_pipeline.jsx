/**
 * Localization Render Pipeline - After Effects Automation
 * 
 * Purpose: Automatically renders localized versions of a video based on a CSV/Table.
 * Inputs: CSV (lang, headline, subtitle, cta, voiceover_path)
 */

(function(thisObj) {
    var scriptName = "Localization Render Pipeline";

    function buildUI(thisObj) {
        var panel = (thisObj instanceof Panel) ? thisObj : new Window("palette", scriptName, undefined, {resizeable: true});
        panel.orientation = "column";
        panel.alignChildren = ["fill", "top"];
        panel.spacing = 10;
        panel.margins = 16;

        var header = panel.add("statictext", undefined, "Localization Render Pipeline");
        header.graphics.font = ScriptUI.newFont("Verdana", "BOLD", 16);

        var helpText = panel.add("statictext", undefined, "Select CSV and target Composition.", {multiline: true});

        // CSV Selection
        var csvGrp = panel.add("group");
        csvGrp.add("statictext", undefined, "Localization CSV:");
        var csvPath = csvGrp.add("edittext", undefined, "Select CSV...");
        csvPath.preferredSize.width = 200;
        var csvBtn = csvGrp.add("button", undefined, "...");

        // Master Comp Selection (Optional - defaults to active)
        var compGrp = panel.add("group");
        compGrp.add("statictext", undefined, "Master Comp Name:");
        var compNameInput = compGrp.add("edittext", undefined, "Master_Comp");
        compNameInput.preferredSize.width = 200;

        var runBtn = panel.add("button", undefined, "GENERATE LOCALIZED VERSIONS");
        runBtn.graphics.backgroundColor = runBtn.graphics.newBrush(runBtn.graphics.BrushType.SOLID_COLOR, [0.2, 0.4, 0.8]);

        // Event Handlers
        csvBtn.onClick = function() {
            var f = File.openDialog("Select Localization CSV");
            if (f) csvPath.text = f.fsName;
        };

        runBtn.onClick = function() {
            var csvFile = new File(csvPath.text);
            var masterCompName = compNameInput.text;

            if (!csvFile.exists) {
                alert("Please select a valid CSV file!");
                return;
            }

            processLocalization(csvFile, masterCompName);
        };

        panel.layout.layout(true);
        return panel;
    }

    function parseCSV(csvFile) {
        csvFile.open("r");
        var content = csvFile.read();
        csvFile.close();

        var lines = content.split(/\r?\n/);
        var data = [];
        var headers = lines[0].split(","); // Assumes comma-separated

        for (var i = 1; i < lines.length; i++) {
            if (lines[i].trim() === "") continue;
            var values = lines[i].split(",");
            var row = {};
            for (var j = 0; j < headers.length; j++) {
                row[headers[j].trim()] = values[j] ? values[j].trim() : "";
            }
            data.push(row);
        }
        return data;
    }

    function processLocalization(csvFile, masterCompName) {
        app.beginUndoGroup("Localization Render Pipeline");

        var localizationData = parseCSV(csvFile);
        var masterComp = null;

        // Find Master Comp
        for (var i = 1; i <= app.project.numItems; i++) {
            if (app.project.item(i) instanceof CompItem && app.project.item(i).name === masterCompName) {
                masterComp = app.project.item(i);
                break;
            }
        }

        if (!masterComp) {
            alert("Master Composition '" + masterCompName + "' not found!");
            return;
        }

        for (var k = 0; k < localizationData.length; k++) {
            var langData = localizationData[k];
            var langCode = langData["lang"] || "Unknown";

            // Duplicate Master Comp for this language
            var localizedComp = masterComp.duplicate();
            localizedComp.name = masterCompName + "_" + langCode;

            // Update Text Layers
            for (var m = 1; m <= localizedComp.numLayers; m++) {
                var layer = localizedComp.layer(m);
                if (layer instanceof TextLayer) {
                    var layerName = layer.name.toLowerCase();
                    if (langData[layerName]) {
                        layer.property("Source Text").setValue(langData[layerName]);
                    }
                }
            }

            // Handle Voiceover (Optional)
            if (langData["voiceover_path"]) {
                var voFile = new File(langData["voiceover_path"]);
                if (voFile.exists) {
                    var voItem = app.project.importFile(new ImportOptions(voFile));
                    var voLayer = localizedComp.layers.add(voItem);
                    voLayer.name = "VO_" + langCode;
                }
            }

            // Add to Render Queue
            app.project.renderQueue.items.add(localizedComp);
        }

        app.endUndoGroup();
        alert("Generated " + localizationData.length + " localized compositions and added to Render Queue.");
    }

    var myPanel = buildUI(thisObj);
    if (myPanel instanceof Window) myPanel.show();

})(this);
