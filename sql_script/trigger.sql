DROP TRIGGER IF EXISTS calculate_final_score;
DELIMITER //
CREATE TRIGGER calculate_final_score BEFORE UPDATE ON `mydb`.`actual_exam_situation`
FOR EACH ROW
BEGIN
  DECLARE correctness_value INT;
  DECLARE fluency_value INT;

  IF NEW.correctness_minus IS NOT NULL THEN
    SET correctness_value = NEW.correctness_minus;
  ELSE
    SET correctness_value = 0;
  END IF;

  IF NEW.fluency_minus IS NOT NULL THEN
    SET fluency_value = NEW.fluency_minus ;
  ELSE
    SET fluency_value = 0;
  END IF;

  IF NEW.correctness_minus IS NOT NULL OR NEW.fluency_minus IS NOT NULL THEN
    SET NEW.final_score = 100 - correctness_value - fluency_value;
  ELSE
    SET NEW.final_score = NULL;
  END IF;
END;

//
DELIMITER ;



