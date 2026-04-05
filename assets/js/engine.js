(() => {
  "use strict";

  const TOOL_ROOT_SELECTOR = "[data-tool-root]";
  const root = document.querySelector(TOOL_ROOT_SELECTOR);

  if (!root) {
    return;
  }

  /**
   * Required data sources supported by this engine:
   *
   * 1) Embedded JSON script tags:
   *    - #tool-questions-json
   *    - #leak-taxonomy-json
   *    - #plug-taxonomy-json
   *    - #scoring-rules-json
   *    - #decision-logic-json
   *
   * 2) Global object:
   *    window.FP_ENGINE_DATA = {
   *      toolQuestions,
   *      leakTaxonomy,
   *      plugTaxonomy,
   *      scoringRules,
   *      decisionLogic
   *    }
   *
   * 3) Fallback:
   *    Questions can be derived from the DOM, but leak/plug/scoring/decision
   *    governance data must still be provided through (1) or (2).
   */

  const state = {
    answers: {},
    questionMap: new Map(),
    moduleMap: new Map(),
    leakMap: new Map(),
    plugMap: new Map(),
    config: null,
  };

  const els = {
    status: root.querySelector("[data-tool-status]"),
    currentModule: root.querySelector("[data-tool-current-module]"),
    progress: root.querySelector("[data-tool-progress]"),
    submit: root.querySelector("[data-tool-submit]"),
    reset: root.querySelector("[data-tool-reset]"),
    resultIntegrityStatus: document.querySelector("[data-result-integrity-status]"),
    resultExecutiveSummary: document.querySelector("[data-result-executive-summary]"),
    resultTotalScore: document.querySelector("[data-result-total-score]"),
    resultBand: document.querySelector("[data-result-band]"),
    resultPrimaryLeak: document.querySelector("[data-result-primary-leak]"),
    resultPrimaryLeakSummary: document.querySelector("[data-result-primary-leak-summary]"),
    resultSecondaryLeak: document.querySelector("[data-result-secondary-leak]"),
    resultSecondaryLeakSummary: document.querySelector("[data-result-secondary-leak-summary]"),
    resultWeakestDimension: document.querySelector("[data-result-weakest-dimension]"),
    resultWeakestDimensionSummary: document.querySelector("[data-result-weakest-dimension-summary]"),
    resultPrimaryPlug: document.querySelector("[data-result-primary-plug]"),
    resultPrimaryPlugSummary: document.querySelector("[data-result-primary-plug-summary]"),
    resultSecondaryPlug: document.querySelector("[data-result-secondary-plug]"),
    resultSecondaryPlugSummary: document.querySelector("[data-result-secondary-plug-summary]"),
    resultInterpretation: document.querySelector("[data-result-interpretation]"),
    dimensionScoreNodes: document.querySelectorAll("[data-dimension-score]"),
    inputs: root.querySelectorAll("[data-question-input]"),
    questionNodes: root.querySelectorAll(".tool-question"),
  };

  const JSON_SCRIPT_IDS = {
    toolQuestions: "tool-questions-json",
    leakTaxonomy: "leak-taxonomy-json",
    plugTaxonomy: "plug-taxonomy-json",
    scoringRules: "scoring-rules-json",
    decisionLogic: "decision-logic-json",
  };

  function setStatus(message) {
    if (els.status) {
      els.status.textContent = message;
    }
  }

  function setCurrentModule(message) {
    if (els.currentModule) {
      els.currentModule.textContent = message;
    }
  }

  function setProgress(percent) {
    if (els.progress) {
      els.progress.textContent = `${percent}%`;
    }
  }

  function readEmbeddedJson(id) {
    const node = document.getElementById(id);
    if (!node) {
      return null;
    }

    try {
      return JSON.parse(node.textContent);
    } catch (error) {
      console.error(`[ENGINE] Invalid JSON in #${id}`, error);
      return null;
    }
  }

  function normalizeWhitespace(value) {
    return String(value || "").replace(/\s+/g, " ").trim();
  }

  function safeRound(value) {
    return Math.round(Number(value || 0));
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function titleFromSlug(slug) {
    return String(slug || "")
      .split("_")
      .join(" ")
      .split("-")
      .join(" ")
      .replace(/\b\w/g, (match) => match.toUpperCase());
  }

  function buildQuestionFromDom(questionNode) {
    const questionId = questionNode.getAttribute("data-question-id");
    const questionOrder = Number(questionNode.getAttribute("data-question-order") || 0);
    const questionType = questionNode.getAttribute("data-question-type") || "scale_1_to_5";
    const required = questionNode.getAttribute("data-question-required") === "true";
    const reverseScored = questionNode.getAttribute("data-question-reverse") === "true";
    const weight = Number(questionNode.getAttribute("data-weight") || 1);

    const moduleSection = questionNode.closest("[data-module-id]");
    const moduleId = moduleSection ? moduleSection.getAttribute("data-module-id") : null;
    const moduleSlug = moduleSection ? moduleSection.getAttribute("data-module-slug") : null;
    const moduleOrder = moduleSection ? Number(moduleSection.getAttribute("data-module-order") || 0) : 0;

    const titleNode = questionNode.querySelector(".structured-list__title");
    const dimensions = String(questionNode.getAttribute("data-dimensions") || "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

    const leakClasses = String(questionNode.getAttribute("data-leak-classes") || "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

    const choiceNodes = questionNode.querySelectorAll("[data-question-input]");
    const choices = Array.from(choiceNodes).map((input) => ({
      value: Number(input.value),
      label: input.getAttribute("data-choice-label") || input.value,
    }));

    return {
      id: questionId,
      order: questionOrder,
      module_id: moduleId,
      module_slug: moduleSlug,
      module_order: moduleOrder,
      label: normalizeWhitespace(titleNode ? titleNode.textContent : questionId),
      type: questionType,
      required,
      reverse_scored: reverseScored,
      dimensions,
      leak_classes: leakClasses,
      weight,
      choices,
    };
  }

  function buildModulesFromDom() {
    const moduleNodes = root.querySelectorAll("[data-module-id]");
    return Array.from(moduleNodes).map((node) => {
      const titleNode = node.querySelector(".section-title");
      const subtitleNode = node.querySelector(".section-subtitle");

      return {
        id: node.getAttribute("data-module-id"),
        slug: node.getAttribute("data-module-slug"),
        order: Number(node.getAttribute("data-module-order") || 0),
        title: normalizeWhitespace(titleNode ? titleNode.textContent : node.getAttribute("data-module-id")),
        description: normalizeWhitespace(subtitleNode ? subtitleNode.textContent : ""),
      };
    });
  }

  function deriveQuestionsFromDom() {
    return Array.from(els.questionNodes).map(buildQuestionFromDom).sort((a, b) => a.order - b.order);
  }

  function getPayloadFromWindow() {
    if (!window.FP_ENGINE_DATA || typeof window.FP_ENGINE_DATA !== "object") {
      return null;
    }
    return window.FP_ENGINE_DATA;
  }

  function loadGovernancePayload() {
    const windowPayload = getPayloadFromWindow();

    const embedded = {
      toolQuestions: readEmbeddedJson(JSON_SCRIPT_IDS.toolQuestions),
      leakTaxonomy: readEmbeddedJson(JSON_SCRIPT_IDS.leakTaxonomy),
      plugTaxonomy: readEmbeddedJson(JSON_SCRIPT_IDS.plugTaxonomy),
      scoringRules: readEmbeddedJson(JSON_SCRIPT_IDS.scoringRules),
      decisionLogic: readEmbeddedJson(JSON_SCRIPT_IDS.decisionLogic),
    };

    const payload = {
      toolQuestions:
        (windowPayload && windowPayload.toolQuestions) ||
        embedded.toolQuestions ||
        null,
      leakTaxonomy:
        (windowPayload && windowPayload.leakTaxonomy) ||
        embedded.leakTaxonomy ||
        null,
      plugTaxonomy:
        (windowPayload && windowPayload.plugTaxonomy) ||
        embedded.plugTaxonomy ||
        null,
      scoringRules:
        (windowPayload && windowPayload.scoringRules) ||
        embedded.scoringRules ||
        null,
      decisionLogic:
        (windowPayload && windowPayload.decisionLogic) ||
        embedded.decisionLogic ||
        null,
    };

    if (!payload.toolQuestions) {
      payload.toolQuestions = {
        questions: deriveQuestionsFromDom(),
        modules: buildModulesFromDom(),
      };
    }

    return payload;
  }

  function validatePayload(payload) {
    const problems = [];

    const questionList = Array.isArray(payload.toolQuestions?.questions)
      ? payload.toolQuestions.questions
      : [];
    const moduleList = Array.isArray(payload.toolQuestions?.modules)
      ? payload.toolQuestions.modules
      : [];

    if (!questionList.length) {
      problems.push("tool questions are missing");
    }
    if (!moduleList.length) {
      problems.push("tool modules are missing");
    }
    if (!Array.isArray(payload.leakTaxonomy?.leak_classes) || !payload.leakTaxonomy.leak_classes.length) {
      problems.push("leak taxonomy is missing");
    }
    if (!Array.isArray(payload.plugTaxonomy?.plug_classes) || !payload.plugTaxonomy.plug_classes.length) {
      problems.push("plug taxonomy is missing");
    }
    if (!Array.isArray(payload.scoringRules?.dimension_scoring?.dimensions) || !payload.scoringRules.dimension_scoring.dimensions.length) {
      problems.push("dimension scoring rules are missing");
    }
    if (!Array.isArray(payload.scoringRules?.leak_signal_scoring?.leak_classes) || !payload.scoringRules.leak_signal_scoring.leak_classes.length) {
      problems.push("leak signal scoring rules are missing");
    }
    if (!Array.isArray(payload.scoringRules?.integrity_bands) || !payload.scoringRules.integrity_bands.length) {
      problems.push("integrity bands are missing");
    }
    if (!payload.decisionLogic?.diagnostic_resolution) {
      problems.push("decision logic is missing");
    }

    return problems;
  }

  function buildMaps(payload) {
    const questions = payload.toolQuestions.questions || [];
    const modules = payload.toolQuestions.modules || [];
    const leaks = payload.leakTaxonomy.leak_classes || [];
    const plugs = payload.plugTaxonomy.plug_classes || [];

    state.questionMap = new Map(questions.map((question) => [question.id, question]));
    state.moduleMap = new Map(modules.map((module) => [module.id, module]));
    state.leakMap = new Map(leaks.map((leak) => [leak.id, leak]));
    state.plugMap = new Map(plugs.map((plug) => [plug.id, plug]));
  }

  function getRequiredQuestionIds() {
    return Array.from(state.questionMap.values())
      .filter((question) => question.required)
      .map((question) => question.id);
  }

  function getAnsweredCount() {
    return Object.keys(state.answers).filter((questionId) => {
      const value = state.answers[questionId];
      return Number.isFinite(value) && state.questionMap.has(questionId);
    }).length;
  }

  function getProgressPercent() {
    const requiredIds = getRequiredQuestionIds();
    if (!requiredIds.length) {
      return 0;
    }

    const answeredRequired = requiredIds.filter((questionId) => Number.isFinite(state.answers[questionId])).length;
    return safeRound((answeredRequired / requiredIds.length) * 100);
  }

  function getCurrentModuleLabel() {
    const questions = Array.from(state.questionMap.values()).sort((a, b) => a.order - b.order);
    const unanswered = questions.find((question) => question.required && !Number.isFinite(state.answers[question.id]));
    if (!unanswered) {
      return `${state.moduleMap.size} / ${state.moduleMap.size}`;
    }

    const module = state.moduleMap.get(unanswered.module_id);
    if (!module) {
      return `—`;
    }

    return `${module.order} / ${state.moduleMap.size}`;
  }

  function updateSessionIndicators() {
    setProgress(getProgressPercent());
    setCurrentModule(getCurrentModuleLabel());
  }

  function getInputValueScore(questionId) {
    const value = state.answers[questionId];
    return Number.isFinite(value) ? value : null;
  }

  function normalizeAnswerValue(value, reverseScored) {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) {
      return null;
    }

    const bounded = clamp(numeric, 1, 5);

    if (reverseScored) {
      return ((5 - bounded) / 4) * 100;
    }

    return ((bounded - 1) / 4) * 100;
  }

  function computeWeightedAverage(questionRules) {
    let weightedSum = 0;
    let totalWeight = 0;

    questionRules.forEach((rule) => {
      const rawValue = getInputValueScore(rule.id);
      if (!Number.isFinite(rawValue)) {
        return;
      }

      const normalized = normalizeAnswerValue(rawValue, Boolean(rule.reverse_scored));
      const weight = Number(rule.weight || 1);

      if (!Number.isFinite(normalized) || !Number.isFinite(weight)) {
        return;
      }

      weightedSum += normalized * weight;
      totalWeight += weight;
    });

    if (totalWeight === 0) {
      return null;
    }

    return weightedSum / totalWeight;
  }

  function computeDimensionScores() {
    const dimensionRules = state.config.scoringRules.dimension_scoring.dimensions || [];
    const scores = {};

    dimensionRules.forEach((dimension) => {
      const score = computeWeightedAverage(dimension.questions || []);
      scores[dimension.slug] = score;
    });

    return scores;
  }

  function computeTotalIntegrityScore(dimensionScores) {
    const config = state.config.scoringRules.dimension_scoring.total_integrity_score;
    const weights = config.dimension_weights || {};

    let weightedSum = 0;
    let totalWeight = 0;

    Object.entries(weights).forEach(([slug, weight]) => {
      const score = dimensionScores[slug];
      const numericWeight = Number(weight || 0);

      if (!Number.isFinite(score) || !Number.isFinite(numericWeight) || numericWeight <= 0) {
        return;
      }

      weightedSum += score * numericWeight;
      totalWeight += numericWeight;
    });

    if (totalWeight === 0) {
      return null;
    }

    return weightedSum / totalWeight;
  }

  function resolveIntegrityBand(totalScore) {
    const bands = state.config.scoringRules.integrity_bands || [];
    return (
      bands.find((band) => totalScore >= band.min_score_inclusive && totalScore <= band.max_score_inclusive) ||
      null
    );
  }

  function computeLeakScores() {
    const leakRules = state.config.scoringRules.leak_signal_scoring.leak_classes || [];
    const scores = {};

    leakRules.forEach((leakRule) => {
      const score = computeWeightedAverage(leakRule.questions || []);
      scores[leakRule.id] = score;
    });

    return scores;
  }

  function getSortedLeakEntries(leakScores) {
    return Object.entries(leakScores)
      .filter(([, score]) => Number.isFinite(score))
      .map(([id, score]) => ({ id, score }))
      .sort((a, b) => a.score - b.score);
  }

  function applyUpstreamOverride(primary, secondary, leakScores, totalScore) {
    const upstream = state.config.decisionLogic.diagnostic_resolution?.upstream_override;
    if (!upstream?.enabled || !Array.isArray(upstream.rules)) {
      return { primary, secondary, overrideApplied: false };
    }

    let overrideApplied = false;
    let resolvedPrimary = primary;
    let resolvedSecondary = secondary;

    upstream.rules.forEach((rule) => {
      const triggerId = rule.trigger_leak;
      const triggerScore = leakScores[triggerId];

      if (!resolvedPrimary || !Number.isFinite(triggerScore)) {
        return;
      }

      const withinWindow =
        triggerScore <= resolvedPrimary.score + Number(rule.override_window_points || 0);

      const totalIntegrityAllowsOverride = totalScore <= 69;

      if (withinWindow && totalIntegrityAllowsOverride && resolvedPrimary.id !== triggerId) {
        resolvedSecondary = resolvedPrimary;
        resolvedPrimary = { id: triggerId, score: triggerScore };
        overrideApplied = true;
      }
    });

    return {
      primary: resolvedPrimary,
      secondary: resolvedSecondary,
      overrideApplied,
    };
  }

  function resolveLeakState(leakScores, totalScore) {
    const sorted = getSortedLeakEntries(leakScores);
    const resolution = state.config.decisionLogic.diagnostic_resolution;
    const signalLogic = state.config.scoringRules.leak_signal_scoring.selection_logic;

    if (!sorted.length) {
      return {
        primary: null,
        secondary: null,
        dualState: false,
        overrideApplied: false,
      };
    }

    let primary = sorted[0];
    let secondary = sorted[1] || null;

    const overridden = applyUpstreamOverride(primary, secondary, leakScores, totalScore);
    primary = overridden.primary;
    secondary = overridden.secondary;

    const dualThreshold = Number(resolution?.dual_state_resolution?.tie_threshold ?? signalLogic?.tie_handling_threshold ?? 3);
    const dualState =
      Boolean(secondary) &&
      Math.abs(primary.score - secondary.score) <= dualThreshold;

    const secondaryThreshold = Number(
      resolution?.secondary_resolution?.maximum_secondary_score_threshold ??
        signalLogic?.secondary_meaningfulness_threshold ??
        60
    );

    const secondaryAllowed = Boolean(secondary) && (dualState || secondary.score <= secondaryThreshold);

    return {
      primary,
      secondary: secondaryAllowed ? secondary : null,
      dualState,
      overrideApplied: overridden.overrideApplied,
    };
  }

  function getWeakestAndStrongestDimensions(dimensionScores) {
    const entries = Object.entries(dimensionScores)
      .filter(([, score]) => Number.isFinite(score))
      .map(([slug, score]) => ({ slug, score }))
      .sort((a, b) => a.score - b.score);

    return {
      weakest: entries[0] || null,
      strongest: entries.length ? entries[entries.length - 1] : null,
    };
  }

  function getDimensionLabel(slug) {
    const dimensions = state.config.scoringRules.dimension_scoring.dimensions || [];
    const found = dimensions.find((dimension) => dimension.slug === slug);
    return found ? found.title : titleFromSlug(slug);
  }

  function resolveDimensionState(score) {
    const bands = state.config.decisionLogic.dimension_state_logic?.bands || [];
    return (
      bands.find((band) => score >= band.min_score_inclusive && score <= band.max_score_inclusive) ||
      null
    );
  }

  function getLeakById(id) {
    return state.leakMap.get(id) || null;
  }

  function getPlugById(id) {
    return state.plugMap.get(id) || null;
  }

  function mapPrimaryPlug(primaryLeakId) {
    const mappings = state.config.scoringRules.plug_recommendation_mapping?.mappings || [];
    const mapping = mappings.find((item) => item.leak_class === primaryLeakId);
    return mapping ? mapping.primary_plug_class : null;
  }

  function mapSecondaryPlug(primaryLeakId, secondaryLeakId) {
    if (!secondaryLeakId) {
      return null;
    }

    const mappings = state.config.scoringRules.plug_recommendation_mapping?.mappings || [];
    const primaryMapping = mappings.find((item) => item.leak_class === primaryLeakId);
    const secondaryMapping = mappings.find((item) => item.leak_class === secondaryLeakId);

    if (!primaryMapping || !secondaryMapping) {
      return null;
    }

    if (!Array.isArray(primaryMapping.secondary_candidates)) {
      return null;
    }

    if (primaryMapping.secondary_candidates.includes(secondaryMapping.primary_plug_class)) {
      return secondaryMapping.primary_plug_class;
    }

    return null;
  }

  function getReportStateConfig(integrityBandSlug) {
    const states = state.config.decisionLogic.report_state_logic?.integrity_status_mapping || [];
    return states.find((item) => item.integrity_band_slug === integrityBandSlug) || null;
  }

  function getExecutiveOpener(reportStateSlug) {
    return state.config.decisionLogic.interpretation_templates?.executive_openers?.[reportStateSlug] || "";
  }

  function getWeakestDimensionSentence(slug) {
    return state.config.decisionLogic.interpretation_templates?.weakest_dimension_templates?.[slug] || "";
  }

  function getPairTemplate(primaryId, secondaryId) {
    const templates = state.config.decisionLogic.interpretation_templates?.primary_secondary_templates || [];
    return templates.find((item) => item.primary === primaryId && item.secondary === secondaryId) || null;
  }

  function buildInterpretationBlock(result) {
    const parts = [];

    if (result.executiveOpener) {
      parts.push(result.executiveOpener);
    }

    if (result.weakestDimensionSentence) {
      parts.push(result.weakestDimensionSentence);
    }

    if (result.primaryLeak && result.primaryLeak.diagnostic_interpretation?.expanded) {
      parts.push(result.primaryLeak.diagnostic_interpretation.expanded);
    }

    if (result.secondaryLeak) {
      const pairTemplate = getPairTemplate(result.primaryLeak.id, result.secondaryLeak.id);
      if (pairTemplate?.template) {
        parts.push(pairTemplate.template);
      } else {
        const fallback = state.config.decisionLogic.interpretation_templates?.fallback_secondary_template;
        if (fallback) {
          parts.push(fallback);
        }
      }
    } else {
      const singleTemplate = state.config.decisionLogic.interpretation_templates?.single_state_template;
      if (singleTemplate) {
        parts.push(singleTemplate);
      }
    }

    if (result.primaryPlug && result.primaryPlug.output_templates?.next_step_sentence) {
      parts.push(result.primaryPlug.output_templates.next_step_sentence);
    }

    return parts.filter(Boolean).join(" ");
  }

  function computeResult() {
    const dimensionScores = computeDimensionScores();
    const totalScore = computeTotalIntegrityScore(dimensionScores);
    const integrityBand = resolveIntegrityBand(totalScore);

    const weakestStrongest = getWeakestAndStrongestDimensions(dimensionScores);
    const leakScores = computeLeakScores();
    const leakState = resolveLeakState(leakScores, totalScore);

    const primaryLeak = leakState.primary ? getLeakById(leakState.primary.id) : null;
    const secondaryLeak = leakState.secondary ? getLeakById(leakState.secondary.id) : null;

    const primaryPlugId = primaryLeak ? mapPrimaryPlug(primaryLeak.id) : null;
    const secondaryPlugId =
      primaryLeak && secondaryLeak ? mapSecondaryPlug(primaryLeak.id, secondaryLeak.id) : null;

    const primaryPlug = primaryPlugId ? getPlugById(primaryPlugId) : null;
    const secondaryPlug =
      secondaryPlugId && secondaryPlugId !== primaryPlugId ? getPlugById(secondaryPlugId) : null;

    const reportState = integrityBand ? getReportStateConfig(integrityBand.slug) : null;
    const executiveOpener = reportState ? getExecutiveOpener(reportState.report_state_slug) : "";
    const weakestDimensionSentence = weakestStrongest.weakest
      ? getWeakestDimensionSentence(weakestStrongest.weakest.slug)
      : "";

    return {
      totalScore,
      integrityBand,
      reportState,
      dimensionScores,
      weakestDimension: weakestStrongest.weakest,
      strongestDimension: weakestStrongest.strongest,
      leakScores,
      primaryLeak,
      primaryLeakScore: leakState.primary ? leakState.primary.score : null,
      secondaryLeak,
      secondaryLeakScore: leakState.secondary ? leakState.secondary.score : null,
      dualState: leakState.dualState,
      overrideApplied: leakState.overrideApplied,
      primaryPlug,
      secondaryPlug,
      executiveOpener,
      weakestDimensionSentence,
    };
  }

  function renderDimensions(dimensionScores) {
    els.dimensionScoreNodes.forEach((node) => {
      const slug = node.getAttribute("data-dimension-score");
      const score = dimensionScores[slug];
      node.textContent = Number.isFinite(score) ? String(safeRound(score)) : "—";
    });
  }

  function renderResult(result) {
    const integrityTitle = result.integrityBand ? result.integrityBand.title : "Unavailable";
    const bandInterpretation = result.integrityBand
      ? result.integrityBand.interpretation
      : "The integrity band could not be resolved from the current input state.";

    if (els.resultIntegrityStatus) {
      els.resultIntegrityStatus.textContent = integrityTitle;
    }

    if (els.resultExecutiveSummary) {
      els.resultExecutiveSummary.textContent =
        result.executiveOpener || "The interpretive report could not be resolved.";
    }

    if (els.resultTotalScore) {
      els.resultTotalScore.textContent = Number.isFinite(result.totalScore)
        ? `${safeRound(result.totalScore)} / 100`
        : "—";
    }

    if (els.resultBand) {
      els.resultBand.textContent = bandInterpretation;
    }

    renderDimensions(result.dimensionScores);

    if (els.resultPrimaryLeak) {
      els.resultPrimaryLeak.textContent = result.primaryLeak ? result.primaryLeak.title : "—";
    }

    if (els.resultPrimaryLeakSummary) {
      els.resultPrimaryLeakSummary.textContent = result.primaryLeak
        ? result.primaryLeak.output_templates?.summary_sentence || result.primaryLeak.description
        : "The primary leak class could not be resolved.";
    }

    if (els.resultSecondaryLeak) {
      els.resultSecondaryLeak.textContent = result.secondaryLeak ? result.secondaryLeak.title : "Not materially meaningful";
    }

    if (els.resultSecondaryLeakSummary) {
      if (result.secondaryLeak) {
        if (result.dualState) {
          els.resultSecondaryLeakSummary.textContent =
            "A co-dominant secondary structural weakness is present and should be treated as materially significant.";
        } else {
          els.resultSecondaryLeakSummary.textContent =
            result.secondaryLeak.output_templates?.summary_sentence || result.secondaryLeak.description;
        }
      } else {
        els.resultSecondaryLeakSummary.textContent =
          "A secondary leak class is not materially meaningful under the current scoring state.";
      }
    }

    if (els.resultWeakestDimension) {
      els.resultWeakestDimension.textContent = result.weakestDimension
        ? getDimensionLabel(result.weakestDimension.slug)
        : "—";
    }

    if (els.resultWeakestDimensionSummary) {
      if (result.weakestDimension) {
        const dimensionState = resolveDimensionState(result.weakestDimension.score);
        const stateMeaning = dimensionState ? dimensionState.meaning : "";
        const sentence = result.weakestDimensionSentence || "";
        els.resultWeakestDimensionSummary.textContent = [sentence, stateMeaning].filter(Boolean).join(" ");
      } else {
        els.resultWeakestDimensionSummary.textContent =
          "The weakest structural dimension could not be resolved.";
      }
    }

    if (els.resultPrimaryPlug) {
      els.resultPrimaryPlug.textContent = result.primaryPlug ? result.primaryPlug.title : "—";
    }

    if (els.resultPrimaryPlugSummary) {
      els.resultPrimaryPlugSummary.textContent = result.primaryPlug
        ? result.primaryPlug.output_templates?.summary_sentence || result.primaryPlug.description
        : "The primary intervention class could not be resolved.";
    }

    if (els.resultSecondaryPlug) {
      els.resultSecondaryPlug.textContent = result.secondaryPlug ? result.secondaryPlug.title : "Not required";
    }

    if (els.resultSecondaryPlugSummary) {
      els.resultSecondaryPlugSummary.textContent = result.secondaryPlug
        ? result.secondaryPlug.output_templates?.summary_sentence || result.secondaryPlug.description
        : "A secondary intervention class is not required or would be redundant under the current diagnostic state.";
    }

    if (els.resultInterpretation) {
      els.resultInterpretation.textContent = buildInterpretationBlock(result);
    }
  }

  function focusFirstMissingQuestion() {
    const requiredQuestionIds = getRequiredQuestionIds();

    for (const questionId of requiredQuestionIds) {
      if (!Number.isFinite(state.answers[questionId])) {
        const node = root.querySelector(`[data-question-id="${questionId}"]`);
        if (node) {
          node.scrollIntoView({ behavior: "smooth", block: "center" });
        }
        return;
      }
    }
  }

  function validateBeforeSubmit() {
    const missing = getRequiredQuestionIds().filter((questionId) => !Number.isFinite(state.answers[questionId]));
    return {
      ok: missing.length === 0,
      missing,
    };
  }

  function resetResultState() {
    if (els.resultIntegrityStatus) {
      els.resultIntegrityStatus.textContent = "Awaiting declared conditions";
    }
    if (els.resultExecutiveSummary) {
      els.resultExecutiveSummary.textContent =
        "Complete the diagnostic sequence to produce the structural report.";
    }
    if (els.resultTotalScore) {
      els.resultTotalScore.textContent = "—";
    }
    if (els.resultBand) {
      els.resultBand.textContent =
        "The score band will be resolved through the governed scoring framework.";
    }
    if (els.resultPrimaryLeak) {
      els.resultPrimaryLeak.textContent = "—";
    }
    if (els.resultPrimaryLeakSummary) {
      els.resultPrimaryLeakSummary.textContent =
        "The dominant structural weakness will appear here.";
    }
    if (els.resultSecondaryLeak) {
      els.resultSecondaryLeak.textContent = "—";
    }
    if (els.resultSecondaryLeakSummary) {
      els.resultSecondaryLeakSummary.textContent =
        "A secondary class will appear only when diagnostically meaningful.";
    }
    if (els.resultWeakestDimension) {
      els.resultWeakestDimension.textContent = "—";
    }
    if (els.resultWeakestDimensionSummary) {
      els.resultWeakestDimensionSummary.textContent =
        "The weakest structural dimension will be resolved after scoring.";
    }
    if (els.resultPrimaryPlug) {
      els.resultPrimaryPlug.textContent = "—";
    }
    if (els.resultPrimaryPlugSummary) {
      els.resultPrimaryPlugSummary.textContent =
        "The primary intervention class will appear here.";
    }
    if (els.resultSecondaryPlug) {
      els.resultSecondaryPlug.textContent = "—";
    }
    if (els.resultSecondaryPlugSummary) {
      els.resultSecondaryPlugSummary.textContent =
        "A secondary intervention class will appear only if it is materially meaningful and non-redundant.";
    }
    if (els.resultInterpretation) {
      els.resultInterpretation.textContent =
        "The interpretive summary will be generated through the governed decision layer once the declared conditions are complete.";
    }
    renderDimensions({
      trust_integrity: null,
      flow_continuity: null,
      decision_clarity: null,
      friction_containment: null,
      recovery_readiness: null,
    });
  }

  function handleInputChange(event) {
    const input = event.target;
    if (!(input instanceof HTMLInputElement)) {
      return;
    }

    if (!input.name) {
      return;
    }

    state.answers[input.name] = Number(input.value);
    updateSessionIndicators();
    setStatus("In progress");
  }

  function bindEvents() {
    els.inputs.forEach((input) => {
      input.addEventListener("change", handleInputChange);
    });

    if (els.reset) {
      els.reset.addEventListener("click", () => {
        state.answers = {};
        els.inputs.forEach((input) => {
          input.checked = false;
        });
        updateSessionIndicators();
        resetResultState();
        setStatus("Ready");
      });
    }

    if (els.submit) {
      els.submit.addEventListener("click", () => {
        const validation = validateBeforeSubmit();

        if (!validation.ok) {
          setStatus(`Incomplete: ${validation.missing.length} required response(s) remain.`);
          focusFirstMissingQuestion();
          return;
        }

        const result = computeResult();
        renderResult(result);
        updateSessionIndicators();
        setStatus("Report generated");
      });
    }
  }

  function initialize() {
    const payload = loadGovernancePayload();
    const problems = validatePayload(payload);

    if (problems.length) {
      console.error("[ENGINE] Governance payload invalid:", problems);
      setStatus("Blocked");
      setCurrentModule("—");
      setProgress(0);
      if (els.resultInterpretation) {
        els.resultInterpretation.textContent =
          `The instrument cannot initialize because governed data is incomplete: ${problems.join("; ")}.`;
      }
      return;
    }

    state.config = payload;
    buildMaps(payload);
    bindEvents();
    updateSessionIndicators();
    resetResultState();
    setStatus("Ready");
  }

  initialize();
})();
