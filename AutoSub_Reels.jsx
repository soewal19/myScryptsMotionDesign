/**
 * AutoSub Reels - Professional After Effects Subtitle Script
 * 
 * Developed by: Senior Script Developer (AI Assistant)
 * Purpose: Professional transcription-to-subtitle workflow for Reels/TikTok/Shorts.
 * Features: SRT import, Word-by-word splitting, Pop animation, Auto-Background, Custom UI.
 */

(function(thisObj) {
    var scriptName = "AutoSub Reels";
    var version = "1.1.0";

    // --- UTILS ---
    function parseSRT(srtContent) {
        var subtitles = [];
        var regex = /(\d+)\r?\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\r?\n([\s\S]*?)(?=\n\r?\n|\n?$)/g;
        var match;

        while ((match = regex.exec(srtContent)) !== null) {
            subtitles.push({
                index: parseInt(match[1]),
                start: timeToSeconds(match[2]),
                end: timeToSeconds(match[3]),
                text: match[4].replace(/\r?\n/g, " ").replace(/<[^>]+>/g, "").trim()
            });
        }
        return subtitles;
    }

    function timeToSeconds(timeStr) {
        var parts = timeStr.split(/[:,]/);
        return parseInt(parts[0]) * 3600 + parseInt(parts[1]) * 60 + parseInt(parts[2]) + parseInt(parts[3]) / 1000;
    }

    function splitIntoWords(sub) {
        var words = sub.text.split(/\s+/);
        if (words.length <= 1) return [sub];

        var result = [];
        var duration = sub.end - sub.start;
        var wordDuration = duration / words.length;

        for (var i = 0; i < words.length; i++) {
            result.push({
                start: sub.start + (i * wordDuration),
                end: sub.start + ((i + 1) * wordDuration),
                text: words[i].toUpperCase() // Reels usually use uppercase
            });
        }
        return result;
    }

    // --- CORE LOGIC ---
    function createSubtitles(subtitles, config) {
        var comp = app.project.activeItem;
        if (!(comp instanceof CompItem)) {
            alert("Please select a composition first!");
            return;
        }

        app.beginUndoGroup("Create Subtitles");

        var subContainer = comp.layers.addNull();
        subContainer.name = "--- SUBTITLES CONTROL ---";
        subContainer.guideLayer = true;

        var processedSubs = [];
        if (config.splitWords) {
            for (var i = 0; i < subtitles.length; i++) {
                var words = splitIntoWords(subtitles[i]);
                for (var j = 0; j < words.length; j++) {
                    processedSubs.push(words[j]);
                }
            }
        } else {
            processedSubs = subtitles;
        }

        for (var i = 0; i < processedSubs.length; i++) {
            var sub = processedSubs[i];
            var textLayer = comp.layers.addText(sub.text);
            
            textLayer.startTime = sub.start;
            textLayer.outPoint = sub.end;
            textLayer.parent = subContainer;

            // Apply Styling
            var textProp = textLayer.property("Source Text");
            var textDocument = textProp.value;
            
            textDocument.fontSize = config.fontSize;
            textDocument.fillColor = config.fillColor;
            textDocument.strokeColor = config.strokeColor;
            textDocument.strokeWidth = config.strokeWidth;
            textDocument.strokeOverFill = true;
            textDocument.applyFill = true;
            textDocument.applyStroke = true;
            textDocument.justification = ParagraphJustification.CENTER_JUSTIFY;
            textDocument.tracking = -20;
            
            if (config.fontName) {
                try {
                    textDocument.font = config.fontName;
                } catch(e) {}
            }

            textProp.setValue(textDocument);

            // Center in Comp
            textLayer.property("Position").setValue([comp.width/2, comp.height * 0.75]);

            // Add Background Box
            if (config.addBg) {
                createBackgroundBox(textLayer, config);
            }

            // Apply Pop Animation
            if (config.applyPop) {
                applyPopAnimation(textLayer);
            }
        }

        app.endUndoGroup();
        alert("Subtitles created: " + processedSubs.length);
    }

    function createBackgroundBox(textLayer, config) {
        var comp = textLayer.containingComp;
        var bgLayer = comp.layers.addShape();
        bgLayer.name = "BG_" + textLayer.name;
        bgLayer.moveAfter(textLayer);
        bgLayer.parent = textLayer;
        bgLayer.startTime = textLayer.startTime;
        bgLayer.outPoint = textLayer.outPoint;

        var shapeGroup = bgLayer.property("Contents").addProperty("ADBE Vector Group");
        var rect = shapeGroup.property("Contents").addProperty("ADBE Vector Shape - Rect");
        var fill = shapeGroup.property("Contents").addProperty("ADBE Vector Graphic - Fill");
        var round = shapeGroup.property("Contents").addProperty("ADBE Vector Filter - RC");

        fill.property("Color").setValue(config.bgColor || [0, 0, 0]);
        fill.property("Opacity").setValue(80);
        round.property("Radius").setValue(20);

        // Expression for auto-size
        var sizeExpr = 
            "var s = thisParent.sourceRectAtTime(); \n" +
            "var pad = " + config.bgPadding + "; \n" +
            "[s.width + pad, s.height + pad];";
        rect.property("Size").expression = sizeExpr;

        var posExpr = 
            "var s = thisParent.sourceRectAtTime(); \n" +
            "[s.left + s.width/2, s.top + s.height/2];";
        shapeGroup.property("Transform").property("Position").expression = posExpr;
    }

    function applyPopAnimation(layer) {
        var scale = layer.property("Scale");
        var expr = 
            "var freq = 3; \n" +
            "var amplitude = 15; \n" +
            "var decay = 5.0; \n" +
            "var t = time - inPoint; \n" +
            "if (t < 0) { value } else { \n" +
            "  var s = amplitude * Math.cos(freq * t * 2 * Math.PI) / Math.exp(decay * t); \n" +
            "  [value[0] + s, value[1] + s]; \n" +
            "}";
        scale.expression = expr;
    }

    // --- UI ---
    function buildUI(thisObj) {
        var panel = (thisObj instanceof Panel) ? thisObj : new Window("palette", scriptName + " v" + version, undefined, {resizeable: true});
        panel.orientation = "column";
        panel.alignChildren = ["fill", "top"];
        panel.spacing = 10;
        panel.margins = 16;

        var titleGrp = panel.add("group");
        titleGrp.alignment = "center";
        var title = titleGrp.add("statictext", undefined, scriptName);
        title.graphics.font = ScriptUI.newFont("Verdana", "BOLD", 18);

        var stylePanel = panel.add("panel", undefined, "Settings");
        stylePanel.orientation = "column";
        stylePanel.alignChildren = ["left", "top"];
        stylePanel.spacing = 8;
        stylePanel.margins = 15;

        var fontGrp = stylePanel.add("group");
        fontGrp.add("statictext", undefined, "Font Size:");
        var sizeInput = fontGrp.add("edittext", undefined, "120");
        sizeInput.characters = 5;

        var splitWordsCheck = stylePanel.add("checkbox", undefined, "Split into individual words (Reels Style)");
        splitWordsCheck.value = true;

        var popCheck = stylePanel.add("checkbox", undefined, "Apply Pop Animation");
        popCheck.value = true;

        var bgCheck = stylePanel.add("checkbox", undefined, "Add Background Box");
        bgCheck.value = true;

        var actionGrp = panel.add("group");
        actionGrp.orientation = "column";
        actionGrp.alignChildren = ["fill", "top"];

        var importBtn = actionGrp.add("button", undefined, "Import SRT & Generate");
        
        // Advanced Section
        var advPanel = panel.add("panel", undefined, "Transcription (Experimental)");
        advPanel.orientation = "column";
        advPanel.alignChildren = ["fill", "top"];
        var apiInput = advPanel.add("edittext", undefined, "OpenAI API Key (optional)");
        var transcribeBtn = advPanel.add("button", undefined, "Transcribe via Whisper API");
        
        transcribeBtn.onClick = function() {
            alert("This feature requires a server-side bridge. Please use the 'Import SRT' method for now, or check the documentation for local Whisper setup.");
        };

        importBtn.onClick = function() {
            var srtFile = File.openDialog("Select SRT file", "*.srt");
            if (!srtFile) return;

            srtFile.open("r");
            var content = srtFile.read();
            srtFile.close();

            var subs = parseSRT(content);
            if (subs.length === 0) {
                alert("Could not parse SRT file.");
                return;
            }

            var config = {
                fontSize: parseInt(sizeInput.text),
                fillColor: [1, 1, 0], // Yellow for Reels
                strokeColor: [0, 0, 0],
                strokeWidth: 10,
                applyPop: popCheck.value,
                splitWords: splitWordsCheck.value,
                addBg: bgCheck.value,
                bgPadding: 40,
                fontName: "Impact"
            };

            createSubtitles(subs, config);
        };

        panel.layout.layout(true);
        return panel;
    }

    var myPanel = buildUI(thisObj);
    if (myPanel instanceof Window) myPanel.show();

})(this);
