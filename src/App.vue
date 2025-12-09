<!-- Window is fixed, 102px, pointer cursor, gradual blurry effect on surrounding words. -->
<!--  Comprehension questions appear afterwards in the same slide -->

<template>
  <Experiment title="Reading Experiment" translate="no">
    <Screen
      :title="'Welcome'"
      class="instructions"
      :validations="{
        SubjectID: {
          minLength: $magpie.v.minLength(2),
        },
      }"
    >
      <!-- <WelcomeScreen /> -->
      <div style="width: 40em; margin: auto">
        <div style="background-color: lightgrey; padding: 10px">
          <b> Information About this Study </b>
        </div>
        <p>
          <br />

          <b>What is being investigated?</b> You are being asked to take part in
          a research study being done at the Massachusetts Institute of
          Technology. This study will help us learn about how people read. It
          will take you around 20 minutes to complete. <br /><br />

          <b>Who can participate?</b> You can participate only if you are an
          adult native speaker of English. <br /><br />

          <b>What am I supposed to do as a participant?</b> If you choose to be
          in the study, you will use the computer mouse to read sentences in
          English and answer questions about them. <br /><br />

          <b>What are my rights during participation?</b> Your participation in
          this study is voluntary. If you choose to participate, you may change
          your mind and leave the study at any time by closing the web page. You
          do not have to provide reasons. <br /><br />

          <b>What risks and benefits can I expect?</b> There are no foreseeable
          risks for participating in this study. <br /><br />

          <b>Will I be compensated for participating?</b> If you complete the
          experiment, you will be compensated for your time according to the
          amount specified on Prolific. <br /><br />

          <b>What data is collected from me and how is it used?</b> During this
          study, we will track the position of your mouse on screen. At the end
          of the study you will be asked to complete a brief survey. No
          personally identifying information will be collected. The data from
          this study may be presented at scientific conferences and published in
          scientific journals, as well as in online repositories. All data will
          remain anonymous. <br /><br />

          <b> Who reviewed this study? </b> This study's protocol has been
          approved by the MIT Committee on the Use of Humans as Experimental
          Subjects. <br /><br />

          <b> Contact: </b> Please feel free to contact us anonymously via
          Prolific Direct Message.
          <br />
        </p>

        <br />
        <div style="background-color: lightgrey; padding: 10px">
          <b> Consent Form </b>
        </div>
        <br />
        I, the participant, confirm by clicking the button below: <br />
        <div style="padding-left: 30px">
          • I have read and understood the study information above.
        </div>
        <div style="padding-left: 30px">
          • I comply with the inclusion and exclusion criteria for participation
          described above.
        </div>
        <div style="padding-left: 30px">
          • I have had enough time to decide about my participation.
        </div>
        <div style="padding-left: 30px">
          • I participate in this study voluntarily and consent that my personal
          data be used as described above.
        </div>
        <div style="padding-left: 30px">
          • I understand that I can stop participating at any moment.
        </div>
        <br />

        <tr>
          <td>Please enter your Prolific ID to continue:&nbsp;</td>
          <td>
            <input
              name="TurkID"
              type="text"
              class="obligatory"
              v-model="$magpie.measurements.SubjectID"
            />
          </td>
        </tr>
        <tr></tr>
      </div>
      <div
        v-if="
          $magpie.measurements.SubjectID &&
          !$magpie.validateMeasurements.SubjectID.$invalid
        "
      >
        <br />
        By clicking on the button below you consent to participating in this
        study:
        <!-- <br /> -->
        <button
          @click="
            $magpie.addExpData({ SubjectId: $magpie.measurements.SubjectID });
            $magpie.nextScreen();
          "
        >
          Proceed
        </button>
      </div>
    </Screen>

    <InstructionScreen :title="'Instructions'">
      <p>
        In this study, you will read sentences. Unlike in normal reading,
        however, the texts will be blurred. In order to bring the text into
        focus, move your mouse over it. When you are done reading, click the
        'Done Reading' button.
      </p>
    </InstructionScreen>

    <InstructionScreen :title="'Instructions'">
      <p>
        Please
        don't worry about punctuation or capitalization, which are not the focus of this study.
      </p>
      <p>
        After reading each sentence, you will be asked a yes-or-no question about the sentence. Indicate your choice by pressing the appropriate
        button.
      </p>
      <p>Press the button to start the study.</p>
    </InstructionScreen>

    <template v-for="(trial, i) of trials">
      <Screen :key="i" class="main_screen" :progress="i / trials.length">
        <Slide>
          <form>
            <input type="hidden" class="item_id" :value="trial.item_id" />
            <input
              type="hidden"
              class="experiment_id"
              :value="trial.experiment_id"
            />
            <input
              type="hidden"
              class="condition_id"
              :value="trial.condition_id"
            />
          </form>
          <div class="oval-cursor"></div>

          <template>
            <div>Sentence {{ i + 1 }} of {{ trials.length }}</div>
          </template>

          <div
            v-if="showFirstDiv"
            class="readingText"
            @mousemove="moveCursor"
            @mouseleave="changeBack"
          >
            <template v-for="(word, index) of trial.text.split(' ')">
              <span :key="index" :data-index="index">
                {{ word }}
              </span>
            </template>
          </div>

          <div
            class="blurry-layer"
            style="
              opacity: 0.3;
              filter: blur(5px);
              transition: all 0.3s linear 0s;
            "
          >
            {{ trial.text }}
          </div>

          <div style="height: 75px"></div>

          <div>
            <button
              v-if="showFirstDiv"
              @click="toggleDivs"
              :disabled="!isCursorMoving"
            >
              Done Reading
            </button>
          </div>

          <div v-if="!showFirstDiv" class="userInput">
            <p>{{ trial.question }}</p>
            <MultipleChoiceInput
              :response.sync="$magpie.measurements.response"
              :options="[trial.answer1, trial.answer2]"
            />
          </div>

          <button
            v-if="$magpie.measurements.response"
            @click="
              toggleDivs();

              const subject_id = $magpie.getAllData()[0].SubjectId;

              $magpie.addTrialData({
                TrialId: i,
                ItemId: trial.item_id,
                Condition: trial.condition_id,
                Experiment: trial.experiment_id,
                TrialText: trial.text,
                TrialType: `comprehensionQuestion`,
                Question: trial.question,
                Answer1: trial.answer1,
                Answer2: trial.answer2,
                userResponse: $magpie.measurements.response,
                ...trial
              });

              const data = $magpie.getAllData();
              const data_filt = data.filter(
                (obj) =>
                  Number(obj.ItemId) === trial.item_id &&
                  obj.Condition === trial.condition_id
              );
              data_filt[0].SubjectId = subject_id;

              $magpie.submitResults($magpie.submissionUrl, data_filt);
              $magpie.nextScreen();
            "
          >
            Next Trial
          </button>
        </Slide>
      </Screen>
    </template>

    <Screen>
      <p>1. Which input device are you using for this experiment?</p>
      <MultipleChoiceInput
        :response.sync="$magpie.measurements.device"
        orientation="horizontal"
        :options="['Computer Mouse', 'Computer Trackpad', 'Other']"
      />
      <br />
      <br />
      <p>2. Which hand are you using during this experiment?</p>
      <MultipleChoiceInput
        :response.sync="$magpie.measurements.hand"
        orientation="horizontal"
        :options="['Left', 'Right', 'Both']"
      />
      <br />
      <br />
      <p>
        What did you think about the experiment? Please describe how hard or
        easy the task felt, anything you noticed about the sentences, or any
        other thoughts you have. If anything was confusing or frustrating,
        please feel free to let us know!
      </p>
      <TextareaInput :response.sync="$magpie.measurements.response" />

      <button
        style="bottom: 30%; transform: translate(-50%, -50%)"
        @click="$magpie.saveAndNextScreen()"
      >
        Submit
      </button>
    </Screen>

    <Screen>
      <p>
        The next screen will submit your results and display your completion
        code.
      </p>

      <button
        style="bottom: 30%; transform: translate(-50%, -50%)"
        @click="
          const data = $magpie.getAllData();
          const subject_id = data[0].SubjectId;
          const last_trial = data[data.length - 1];
          const updated_last_trial = [{ ...last_trial, SubjectId: subject_id }];
          $magpie.submitResults($magpie.submissionUrl, updated_last_trial);
          $magpie.nextScreen();
        "
      >
        Continue
      </button>
    </Screen>

    <!-- <SubmitResultsScreen /> -->

    <Screen :title="'Study Complete'">
      <p class="selectable-text" style="font-size: 24px">Completion Code:</p>
      <p class="selectable-text" style="font-size: 24px">C101RMLG</p>
    </Screen>
  </Experiment>
</template>

<script>
import fillers from "../trials/filler.csv";
import _ from "lodash";

// Get query parameters from URL
const urlParams = new URLSearchParams(window.location.search);
console.log(urlParams);
const listId = urlParams.get('LIST_ID') || '1';
console.log(listId);

// Load data from csv files as javascript arrays with objects
// ensure that listId is zfilled to take up 2 places, e.g. 01, 02, ... 10
const listIdPadded = listId.padStart(2, "0");
// Import all available list files (01-25)
// Import all available list files for the questionnaires
import list01 from "../trials/list_01.csv";
import list02 from "../trials/list_02.csv";
import list03 from "../trials/list_03.csv";
import list04 from "../trials/list_04.csv";
import list05 from "../trials/list_05.csv";
import list06 from "../trials/list_06.csv";
import list07 from "../trials/list_07.csv";
import list08 from "../trials/list_08.csv";
import list09 from "../trials/list_09.csv";
import list10 from "../trials/list_10.csv";
import list11 from "../trials/list_11.csv";
import list12 from "../trials/list_12.csv";
import list13 from "../trials/list_13.csv";
import list14 from "../trials/list_14.csv";
import list15 from "../trials/list_15.csv";
import list16 from "../trials/list_16.csv";
import list17 from "../trials/list_17.csv";
import list18 from "../trials/list_18.csv";
import list19 from "../trials/list_19.csv";
import list20 from "../trials/list_20.csv";
import list21 from "../trials/list_21.csv";
import list22 from "../trials/list_22.csv";
import list23 from "../trials/list_23.csv";
import list24 from "../trials/list_24.csv";
import list25 from "../trials/list_25.csv";

// Create a mapping and select the correct list
const listMap = {
  "01": list01,
  "02": list02,
  "03": list03,
  "04": list04,
  "05": list05,
  "06": list06,
  "07": list07,
  "08": list08,
  "09": list09,
  "10": list10,
  "11": list11,
  "12": list12,
  "13": list13,
  "14": list14,
  "15": list15,
  "16": list16,
  "17": list17,
  "18": list18,
  "19": list19,
  "20": list20,
  "21": list21,
  "22": list22,
  "23": list23,
  "24": list24,
  "25": list25,
};

const list1 = listMap[listIdPadded] || listMap["01"];

export default {
  name: "App",
  data() {
    const showImages = false;

    console.log(list1);

    const updatedItems = _.shuffle(list1).map((trial, idx) => {
      // var col = shuffledConditions[idx];
      return {
        ...trial,
        item_id: trial["Item"],
        text: trial["sentence"],
        condition_id: `${trial["verb_condition"]}_${trial["subject_condition"]}_${trial["context_condition"]}_${trial["predicate_condition"]}`,
        experiment_id: "ncprediction",
        
        // List-specific metadata
        verb_condition: trial["verb_condition"],
        verb: trial["verb"],
        subject_condition: trial["subject_condition"],
        subject: trial["subject"],
        context_condition: trial["context_condition"],
        context: trial["context"],
        predicate_condition: trial["predicate_condition"],
        predicate: trial["predicate"],
        Preamble: trial["Preamble"],
        prefix: trial["prefix"],
        CriticalWord: trial["CriticalWord"],
        intervention_simple: trial["intervention_simple"],
        continuation: trial["continuation"],
        aux: trial["aux"],
        verb_1_o: trial["verb_1_o"],
        question: trial["question"],
        group_id: trial["group_id"],
        answer1: trial["answer1"],
        answer2: trial["answer2"],
        question_delay: trial["question_delay"],
        correct_answer: trial["correct_answer"],
        with_question: trial["with_question"],
        material_id: trial["material_id"],
      };
    });

    const updatedFillers = fillers.map((trial, idx) => {
      return {
        // Essential trial data
        item_id: trial["Item"],
        text: trial["Sentence"],
        condition_id: "filler",
        experiment_id: "ncprediction",
        
        // Filler-specific metadata
        with_question: trial["with_question"],
        question: trial["question"],
        answer1: trial["answer1"],
        answer2: trial["answer2"],
        correct_answer: trial["correct_answer"],
        question_delay: trial["question_delay"],
      };
    });

    // get five clean fillers to ensure we show first -- removes them from the original list
    const updatedFillersCleanPreview = updatedFillers.splice(6, 5);

    // console.log(updatedFillers);

    const updatedShuffledItems = updatedFillersCleanPreview.concat(
      _.shuffle(updatedItems.concat(updatedFillers))
    );
    // const updatedShuffledItems = updatedFillersCleanPreview.concat(
    //   _.sampleSize(_.shuffle(updatedItems.concat(updatedFillers)), 5)
    // );

    // debugging
    console.log(updatedShuffledItems);

    return {
      isCursorMoving: false,
      trials: updatedShuffledItems,
      currentIndex: null,
      showFirstDiv: true,
      mousePosition: {
        x: 0,
        y: 0,
      },
      userResponse: "",
      showImages: showImages,
    };
  },
  computed: {
    console: () => console,
    window: () => window,
  },
  mounted() {
    setInterval(this.saveData, 50);
  },
  methods: {
    changeBack() {
      this.$el.querySelector(".oval-cursor").classList.remove("grow");
      this.$el.querySelector(".oval-cursor").classList.remove("blank");
      this.currentIndex = null;
    },
    saveData() {
      if (this.currentIndex !== null) {
        const currentElement = this.$el.querySelector(
          `span[data-index="${this.currentIndex}"]`
        );
        if (currentElement) {
          const currentElementRect = currentElement.getBoundingClientRect();
          $magpie.addTrialData({
            Experiment: this.$el.querySelector(".experiment_id").value,
            Condition: this.$el.querySelector(".condition_id").value,
            ItemId: this.$el.querySelector(".item_id").value,
            Index: this.currentIndex,
            Word: currentElement.innerHTML,
            mousePositionX: this.mousePosition.x,
            mousePositionY: this.mousePosition.y,
            wordPositionTop: currentElementRect.top,
            wordPositionLeft: currentElementRect.left,
            wordPositionBottom: currentElementRect.bottom,
            wordPositionRight: currentElementRect.right,
            // wordPositionTop: currentElement.offsetTop,
            // wordPositionLeft: currentElement.offsetLeft,
            // wordPositionBottom: currentElement.offsetHeight + currentElement.offsetTop,
            // wordPositionRight: currentElement.offsetWidth + currentElement.offsetLeft
          });
        } else {
          $magpie.addTrialData({
            Experiment: this.$el.querySelector(".experiment_id").value,
            Condition: this.$el.querySelector(".condition_id").value,
            ItemId: this.$el.querySelector(".item_id").value,
            Index: this.currentIndex,
            mousePositionX: this.mousePosition.x,
            mousePositionY: this.mousePosition.y,
          });
        }
      }
    },
    moveCursor(e) {
      this.isCursorMoving = true;
      this.$el.querySelector(".oval-cursor").classList.add("grow");
      let x = e.clientX;
      let y = e.clientY;
      const elementAtCursor = document.elementFromPoint(x, y).closest("span");
      if (elementAtCursor) {
        this.$el.querySelector(".oval-cursor").classList.remove("blank");
        this.currentIndex = elementAtCursor.getAttribute("data-index");
      } else {
        this.$el.querySelector(".oval-cursor").classList.add("blank");
        const elementAboveCursor = document
          .elementFromPoint(x, y - 3)
          .closest("span");
        if (elementAboveCursor) {
          this.currentIndex = elementAboveCursor.getAttribute("data-index");
        } else {
          this.currentIndex = -1;
        }
      }

      this.$el.querySelector(".oval-cursor").style.left = `${x + 12}px`;
      this.$el.querySelector(".oval-cursor").style.top = `${y - 6}px`;
      this.mousePosition.x = e.clientX;
      this.mousePosition.y = e.clientY;
      // this.mousePosition.x = e.offsetX;
      // this.mousePosition.y = e.offsetY;
    },
    toggleDivs() {
      this.showFirstDiv = !this.showFirstDiv;
      this.isCursorMoving = false;
    },
    getScreenDimensions() {
      return {
        window_inner_width: window.innerWidth,
        window_inner_height: window.innerHeight,
      };
    },
  },
};
</script>

<style>
.experiment {
  display: flex;
  align-items: center;
  justify-content: center;
}
.main_screen {
  isolation: isolate;
  position: relative;
  width: 100%;
  height: auto;
  font-size: 18px;
  line-height: 40px;
}
.debugResults {
  width: 100%;
}
.readingText {
  /* z-index: 1; */
  position: absolute;
  color: white;
  text-align: left;
  font-weight: 450;
  cursor: pointer;
  padding-top: 2%;
  padding-bottom: 2%;
  padding-left: 11%;
  padding-right: 11%;
}
.userInput {
  padding-top: 2%;
  padding-bottom: 2%;
  padding-left: 20%;
  padding-right: 20%;
}
button {
  /* position: absolute; */
  /* bottom: 0; */
  left: 50%;
}
.oval-cursor {
  position: fixed;
  z-index: 2;
  width: 1px;
  height: 1px;
  transform: translate(-50%, -50%);
  background-color: white;
  mix-blend-mode: difference;
  border-radius: 50%;
  pointer-events: none;
  transition: width 0.5s, height 0.5s;
}
.oval-cursor.grow.blank {
  width: 80px;
  height: 13px;
}
.oval-cursor.grow {
  width: 102px;
  height: 38px;
  border-radius: 50%;
  box-shadow: 30px 0 8px -4px rgba(255, 255, 255, 0.1),
    -30px 0 8px -4px rgba(255, 255, 255, 0.1);
  background-color: rgba(255, 255, 255, 0.3);
  background-blend-mode: screen;
  pointer-events: none;
  transition: width 0.5s, height 0.5s;
  filter: blur(3px);
}
.oval-cursor.grow::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 70%;
  height: 70%;
  background-color: white;
  mix-blend-mode: normal;
  border-radius: 50%;
}
.blurry-layer {
  position: absolute;
  pointer-events: none;
  color: black;
  text-align: left;
  font-weight: 450;
  padding-top: 2%;
  padding-bottom: 2%;
  padding-left: 11%;
  padding-right: 11%;
}

* {
  user-select: none; /* Standard syntax */
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none; /* Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
}
.selectable-text {
  -webkit-user-select: text; /* Chrome/Safari */
  -moz-user-select: text; /* Firefox */
  -ms-user-select: text; /* IE/Edge */
  user-select: text; /* standard */
}
</style>
