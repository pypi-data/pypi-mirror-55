async function load_data() {

    let loaded_data = await eel.load_data($("#inputDataFileLabel").val())();

    option_chains = loaded_data.foldLeft("", function(acc, element) {
        return acc + '<option value="' + element + '">' + element + '</option>';
    });

    $("select").html(option_chains);
    $("#params-form, #send-form, #log-window").show("400")
    $('.form-check-input').bootstrapToggle()
}


async function generate_data() {
    chain = $("#chain-select").val()
    enviroment = document.getElementById('enviroment-switch').checked ? "LIVE" : "WORK"
    outputs = []
    if (document.getElementById('doc-switch').checked){
        outputs.add("DOC")
    }
    if (document.getElementById('xml-switch').checked){
        outputs.add("XML")
    }
    await eel.generate_data(chain, enviroment, outputs)();

}
