/**
 * Hook Swapper Pro - After Effects Automation
 * 
 * Purpose: Automatically creates multiple video variations by swapping different 3-5s "Hooks"
 * with a single "Master Body" (CTA).
 */

(function(thisObj) {
    var scriptName = "Hook Swapper Pro";

    function buildUI(thisObj) {
        var panel = (thisObj instanceof Panel) ? thisObj : new Window("palette", scriptName, undefined, {resizeable: true});
        panel.orientation = "column";
        panel.alignChildren = ["fill", "top"];
        panel.spacing = 10;
        panel.margins = 16;

        var header = panel.add("statictext", undefined, "Hook Swapper Pro");
        header.graphics.font = ScriptUI.newFont("Verdana", "BOLD", 16);

        var helpText = panel.add("statictext", undefined, "Select Master Body and Hook files to generate variations.", {multiline: true});

        // Master Body Selection
        var masterGrp = panel.add("group");
        masterGrp.add("statictext", undefined, "Master Body:");
        var masterPath = masterGrp.add("edittext", undefined, "Select file...");
        masterPath.preferredSize.width = 200;
        var masterBtn = masterGrp.add("button", undefined, "...");

        // Hooks Selection
        var hooksGrp = panel.add("group");
        hooksGrp.add("statictext", undefined, "Hooks Folder:");
        var hooksPath = hooksGrp.add("edittext", undefined, "Select folder...");
        hooksPath.preferredSize.width = 200;
        var hooksBtn = hooksGrp.add("button", undefined, "...");

        var runBtn = panel.add("button", undefined, "GENERATE VARIATIONS");
        runBtn.graphics.backgroundColor = runBtn.graphics.newBrush(runBtn.graphics.BrushType.SOLID_COLOR, [0.2, 0.6, 0.2]);

        // Event Handlers
        masterBtn.onClick = function() {
            var f = File.openDialog("Select Master Body Video");
            if (f) masterPath.text = f.fsName;
        };

        hooksBtn.onClick = function() {
            var d = Folder.selectDialog("Select Folder with Hooks");
            if (d) hooksPath.text = d.fsName;
        };

        runBtn.onClick = function() {
            var masterFile = new File(masterPath.text);
            var hooksFolder = new Folder(hooksPath.text);

            if (!masterFile.exists || !hooksFolder.exists) {
                alert("Please select valid paths!");
                return;
            }

            processSwapping(masterFile, hooksFolder);
        };

        panel.layout.layout(true);
        return panel;
    }

    function processSwapping(masterFile, hooksFolder) {
        app.beginUndoGroup("Hook Swapping");

        var hookFiles = hooksFolder.getFiles(/\.(mp4|mov|avi|m4v)$/i);
        if (hookFiles.length === 0) {
            alert("No video files found in Hooks folder!");
            return;
        }

        // Import Master
        var masterItem = app.project.importFile(new ImportOptions(masterFile));

        for (var i = 0; i < hookFiles.length; i++) {
            var hookFile = hookFiles[i];
            var hookItem = app.project.importFile(new ImportOptions(hookFile));

            // Create Comp for this variation
            var compName = "Variation_" + hookItem.name.split(".")[0];
            var comp = app.project.items.addComp(compName, masterItem.width, masterItem.height, masterItem.pixelAspect, hookItem.duration + masterItem.duration, masterItem.frameRate);

            // Add Hook Layer
            var hookLayer = comp.layers.add(hookItem);
            hookLayer.startTime = 0;

            // Add Master Body Layer
            var masterLayer = comp.layers.add(masterItem);
            masterLayer.startTime = hookItem.duration;

            // Add to Render Queue (Optional but professional)
            app.project.renderQueue.items.add(comp);
        }

        app.endUndoGroup();
        alert("Generated " + hookFiles.length + " variations in the project and added to Render Queue.");
    }

    var myPanel = buildUI(thisObj);
    if (myPanel instanceof Window) myPanel.show();

})(this);
